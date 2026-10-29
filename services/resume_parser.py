import os
import pdfplumber


def extract_resume_text(filepath):
    """Return plain text from a PDF or TXT resume ('' if nothing extractable)."""
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".txt":
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read().strip()
    text = []
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")   # scanned pages return None
    return "\n".join(text).strip()
