import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from services.skill_extractor import extract_skills
from services.ranker import rank_candidates


def test_extract_skills_word_boundaries():
    assert extract_skills("Built APIs with Flask and Python") == ["flask", "python"]
    assert "java" not in extract_skills("I know javascript")


def test_ranking_prefers_better_match():
    pool = [{"id": "a", "name": "a", "text": "Python Flask SQL developer", "uploaded": False},
            {"id": "b", "name": "b", "text": "Graphic designer using Photoshop", "uploaded": False}]
    ranked, skills = rank_candidates("Need Python, Flask and SQL developer", pool)
    assert ranked[0]["id"] == "a" and ranked[0]["rank"] == 1
    assert set(skills) == {"python", "flask", "sql"}
