import logging
import os
import uuid

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from config import Config
from models import RunResult, ScreeningRun, db
from services.ai_analyzer import analyze_jd
from services.dataset_loader import load_candidates, to_pool
from services.ranker import rank_candidates
from services.resume_parser import extract_resume_text

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    try:
        app.dataset = to_pool(load_candidates(app.config["DATA_PATH"]))
    except OSError:
        log.error("Dataset not found at %s", app.config["DATA_PATH"])
        app.dataset = []
    log.info("Candidates loaded: %d", len(app.dataset))

    def allowed(name):
        return "." in name and name.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

    @app.route("/")
    def home():
        return render_template("index.html", total=len(app.dataset))

    @app.route("/rank", methods=["POST"])
    def rank():
        jd = request.form.get("jd", "").strip()
        if len(jd) < 30:
            flash("Paste a job description of at least 30 characters.")
            return redirect(url_for("home"))

        pool = []
        for f in request.files.getlist("resume"):
            if not f or not f.filename:
                continue
            name = secure_filename(f.filename)
            if not allowed(name):
                flash(f"{f.filename}: only PDF or TXT files are accepted.")
                continue
            path = os.path.join(app.config["UPLOAD_FOLDER"], f"{uuid.uuid4().hex}_{name}")
            f.save(path)
            try:
                text = extract_resume_text(path)
            except Exception:
                log.exception("Could not read %s", name)
                text = ""
            finally:
                os.remove(path)
            if not text:
                flash(f"{name}: no readable text found (scanned PDF?).")
                continue
            pool.append({"id": name, "name": name, "text": text, "uploaded": True})
        pool += app.dataset
        if not pool:
            flash("No candidates available to rank.")
            return redirect(url_for("home"))

        analysis = analyze_jd(jd)
        extra = analysis.get("required_skills", []) if analysis else []
        ranked, jd_skills = rank_candidates(jd, pool, extra,
                                            app.config["SKILL_WEIGHT"], app.config["TEXT_WEIGHT"])
        top = [r for r in ranked if r["rank"] <= app.config["TOP_N"] or r["uploaded"]]

        run = ScreeningRun(job_description=jd, jd_skills=jd_skills, jd_analysis=analysis)
        run.results = [RunResult(rank=r["rank"], candidate_ref=r["id"], name=r["name"],
                                 score=r["score"], skill_score=r["skill_score"],
                                 text_score=r["text_score"], matched=r["matched"],
                                 missing=r["missing"], uploaded=r["uploaded"]) for r in top]
        db.session.add(run)
        db.session.commit()
        return redirect(url_for("view_run", run_id=run.id))

    @app.route("/run/<int:run_id>")
    def view_run(run_id):
        run = db.get_or_404(ScreeningRun, run_id)
        return render_template("result.html", run=run,
                               sw=int(app.config["SKILL_WEIGHT"] * 100),
                               tw=int(app.config["TEXT_WEIGHT"] * 100))

    @app.route("/history")
    def history():
        runs = ScreeningRun.query.order_by(ScreeningRun.created_at.desc()).limit(50).all()
        return render_template("history.html", runs=runs)

    @app.errorhandler(413)
    def too_large(_):
        flash("File too large (max 10 MB).")
        return redirect(url_for("home"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=Config.DEBUG)
