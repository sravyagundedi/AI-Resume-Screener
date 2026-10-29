import json
import logging
import re
from config import Config

log = logging.getLogger(__name__)
PROMPT = """You are a recruiting assistant. Analyze this job description and reply with ONLY JSON:
{{"role": str, "seniority": str, "required_skills": [str], "nice_to_have": [str], "summary": str}}
Use short lowercase skill names (e.g. "python", "docker").

Job description:
{jd}"""


def analyze_jd(jd):
    """Structured JD analysis from Gemini; returns None if unavailable (app keeps working)."""
    if not Config.GEMINI_API_KEY:
        return None
    try:
        from google import genai
        client = genai.Client(api_key=Config.GEMINI_API_KEY)
        resp = client.models.generate_content(
            model="gemini-2.5-flash", contents=PROMPT.format(jd=jd[:6000]),
            config={"response_mime_type": "application/json"})
        data = json.loads(re.sub(r"^```(?:json)?|```$", "", resp.text.strip()).strip())
        return data if isinstance(data, dict) else None
    except Exception as exc:   # network, quota, bad JSON...
        log.warning("Gemini analysis failed: %s", exc)
        return None
