from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ScreeningRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    job_description = db.Column(db.Text)
    jd_skills = db.Column(db.JSON)
    jd_analysis = db.Column(db.JSON)
    results = db.relationship("RunResult", backref="run", cascade="all, delete-orphan",
                              order_by="RunResult.rank")


class RunResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    run_id = db.Column(db.Integer, db.ForeignKey("screening_run.id"))
    rank = db.Column(db.Integer)
    candidate_ref = db.Column(db.String(100))
    name = db.Column(db.String(200))
    score = db.Column(db.Float)
    skill_score = db.Column(db.Float)
    text_score = db.Column(db.Float)
    matched = db.Column(db.JSON)
    missing = db.Column(db.JSON)
    uploaded = db.Column(db.Boolean, default=False)
