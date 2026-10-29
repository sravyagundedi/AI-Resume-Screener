import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
_FULL = os.path.join(BASE_DIR, "data", "candidates.jsonl")
_SAMPLE = os.path.join(BASE_DIR, "data", "sample_candidates.jsonl")

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "candidate.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    DATA_PATH = _FULL if os.path.exists(_FULL) else _SAMPLE
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"pdf", "txt"}
    SKILL_WEIGHT = 0.6   # share of final score from skill overlap
    TEXT_WEIGHT = 0.4    # share from TF-IDF similarity
    TOP_N = 10
