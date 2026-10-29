import re

SKILLS = {
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "sql", "nosql",
    "html", "css", "react", "angular", "vue", "node.js", "express", "flask", "django",
    "fastapi", "spring", "mysql", "postgresql", "mongodb", "redis", "sqlite",
    "machine learning", "deep learning", "nlp", "computer vision", "data analysis",
    "data science", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras",
    "opencv", "tableau", "power bi", "excel", "statistics", "aws", "azure", "gcp",
    "docker", "kubernetes", "git", "github", "linux", "ci/cd", "jenkins", "terraform",
    "rest api", "graphql", "microservices", "agile", "scrum", "jira", "spark", "hadoop",
    "kafka", "airflow", "etl", "llm", "generative ai", "langchain", "android", "ios",
    "swift", "kotlin", "flutter", "selenium", "testing", "pytest", "devops", "cybersecurity",
    "communication", "leadership", "problem solving",
}


def extract_skills(text, extra=()):
    """Return the sorted skills from the vocabulary (plus extras) found in text."""
    if not text:
        return []
    low = text.lower()
    vocab = SKILLS | {s.lower().strip() for s in extra if isinstance(s, str) and len(s.strip()) > 1}
    found = set()
    for skill in vocab:
        pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"
        if re.search(pattern, low):
            found.add(skill)
    return sorted(found)
