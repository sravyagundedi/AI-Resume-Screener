from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def batch_similarity(job_description, texts):
    """Fit TF-IDF once on JD + all texts; return one cosine score per text."""
    if not job_description or not texts:
        return [0.0] * len(texts)
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    try:
        matrix = vectorizer.fit_transform([job_description] + list(texts))
    except ValueError:   # empty vocabulary
        return [0.0] * len(texts)
    return [float(s) for s in cosine_similarity(matrix[0:1], matrix[1:])[0]]
