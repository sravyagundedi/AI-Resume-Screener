# AI Resume Screening System (Code-A-Nova, Level 1a)

Flask app that extracts resume text, matches skills against a job description, and ranks candidates.

## Features
- **Resume text extraction**: PDF/TXT upload parsed with pdfplumber (multiple resumes at once).
- **Skill matching**: vocabulary-based skill extraction; shows matched and missing skills per candidate. Gemini optionally adds JD-specific skills.
- **Ranking**: `score = 0.6 x skill overlap + 0.4 x TF-IDF cosine similarity` (weights in `config.py`). TF-IDF is fit once for all candidates.
- **History**: every run is stored in SQLite and viewable at `/history`.
- Works without a Gemini key (AI analysis is skipped gracefully).

## Setup
```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                              # add GEMINI_API_KEY (optional)
python app.py                                     # http://127.0.0.1:5000
pytest
```

## Structure
`app.py` routes, `services/` (parsing, skills, similarity, ranking, Gemini), `models.py` DB, `templates/` + `static/` UI, `data/candidates.jsonl` dataset, `tests/`.

## Flow
Upload resumes + paste JD, extract text, extract JD skills (vocab + Gemini), score every candidate, save run, show results.
