from services.similarity import batch_similarity
from services.skill_extractor import extract_skills


def rank_candidates(jd, pool, extra_skills=(), skill_weight=0.6, text_weight=0.4):
    """Score every candidate in pool and return (ranked list, jd_skills); scores in %."""
    jd_skills = extract_skills(jd, extra_skills)
    text_scores = batch_similarity(jd, [c["text"] for c in pool])
    if not jd_skills:                       # nothing to match on: use text similarity only
        skill_weight, text_weight = 0.0, 1.0
    results = []
    for cand, tscore in zip(pool, text_scores):
        have = set(extract_skills(cand["text"], extra_skills))
        matched = sorted(have & set(jd_skills))
        missing = sorted(set(jd_skills) - have)
        sscore = len(matched) / len(jd_skills) if jd_skills else 0.0
        final = skill_weight * sscore + text_weight * tscore
        results.append({**cand, "matched": matched, "missing": missing,
                        "skill_score": round(sscore * 100, 1),
                        "text_score": round(tscore * 100, 1),
                        "score": round(final * 100, 1)})
    results.sort(key=lambda r: r["score"], reverse=True)
    for i, r in enumerate(results, 1):
        r["rank"] = i
    return results, jd_skills
