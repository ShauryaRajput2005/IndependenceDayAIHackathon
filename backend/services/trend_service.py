"""
services/trend_service.py — Load and filter curated trend/meme format data.
"""
import json
import os
from typing import List

from utils.logger import get_logger

logger = get_logger(__name__)

_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def _load_json(filename: str) -> list:
    path = os.path.join(_DATA_DIR, filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        logger.error("Failed to load %s: %s", filename, exc)
        return []


def get_relevant_trends(
    platform: str = "",
    tone: str = "",
    audience: str = "",
    limit: int = 4,
) -> List[dict]:
    """
    Return curated trends filtered by platform, tone, and audience.
    Falls back to all trends if no match.
    """
    all_trends = _load_json("trends.json")
    platform_l = platform.lower()
    tone_l = tone.lower()

    scored: List[tuple] = []
    for trend in all_trends:
        score = 0
        if platform_l and platform_l in [p.lower() for p in trend.get("platforms", [])]:
            score += 2
        if tone_l and any(tone_l in t.lower() for t in trend.get("tones", [])):
            score += 2
        if audience and any(
            part in trend.get("audience", []) for part in audience.split()
        ):
            score += 1
        scored.append((score, trend))

    scored.sort(key=lambda x: x[0], reverse=True)
    results = [t for _, t in scored[:limit]]
    return results if results else all_trends[:limit]


def get_relevant_meme_formats(
    tone: str = "",
    audience: str = "",
    limit: int = 4,
) -> List[dict]:
    """Return curated meme formats filtered by tone and audience."""
    all_memes = _load_json("meme_formats.json")
    tone_l = tone.lower()

    scored: List[tuple] = []
    for meme in all_memes:
        score = 0
        best_for = [b.lower() for b in meme.get("best_for", [])]
        if tone_l and any(tone_l in b for b in best_for):
            score += 2
        if audience:
            audience_words = audience.lower().split()
            for aw in audience_words:
                if any(aw in a.lower() for a in meme.get("audience", [])):
                    score += 1
        scored.append((score, meme))

    scored.sort(key=lambda x: x[0], reverse=True)
    results = [m for _, m in scored[:limit]]
    return results if results else all_memes[:limit]


def format_trends_for_prompt(trends: List[dict]) -> str:
    if not trends:
        return "No trend data available."
    lines = []
    for t in trends:
        lines.append(f"• {t['name']}: {t.get('description', '')}")
        lines.append(f"  Best for: {t.get('best_for', '')}")
        if t.get("example"):
            lines.append(f"  Example: {t['example']}")
    return "\n".join(lines)
