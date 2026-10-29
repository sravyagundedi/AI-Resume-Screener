import json
import logging

log = logging.getLogger(__name__)


def load_candidates(path):
    """Read a JSON-lines file; skip malformed lines instead of crashing."""
    candidates = []
    with open(path, "r", encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                candidates.append(json.loads(line))
            except json.JSONDecodeError:
                log.warning("Skipping bad JSON on line %d", n)
    return candidates


def _flatten(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [s for v in value for s in _flatten(v)]
    if isinstance(value, dict):
        return [s for v in value.values() for s in _flatten(v)]
    return []


def to_pool(candidates):
    """Convert raw records into {id, name, text, uploaded} dicts."""
    pool = []
    for c in candidates:
        profile = c.get("profile") or {}
        parts = [profile.get("headline", ""), profile.get("summary", "")]
        parts += _flatten(profile.get("skills", c.get("skills", [])))
        parts += _flatten(profile.get("experience", c.get("experience", [])))
        text = " ".join(p for p in parts if p).strip()
        if not text:
            continue
        cid = str(c.get("candidate_id", len(pool)))
        pool.append({"id": cid, "name": (profile.get("headline") or cid)[:80],
                     "text": text, "uploaded": False})
    return pool
