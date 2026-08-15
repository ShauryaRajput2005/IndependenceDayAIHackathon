import os
from typing import Any

from utils.json_parser import parse_json_object


MEDIA_TYPES = {"gif", "meme", "sticker", "clip", "emoji"}


def _safe_failure_reason(prefix: str, error: Exception) -> str:
    response = getattr(error, "response", None)
    status_code = getattr(response, "status_code", None)
    if status_code:
        return f"{prefix} failed with HTTP {status_code}."
    return f"{prefix} failed: {error.__class__.__name__}."


def _fallback_media_type(content: dict[str, Any], tone: str) -> str:
    text = " ".join(
        [
            str(tone),
            str(content.get("hook", "")),
            str(content.get("meme_format", "")),
            str(content.get("caption", "")),
            str(content.get("klipy_query", "")),
        ]
    ).lower()
    if any(word in text for word in ["emotional", "story", "cinematic", "transformation", "luxury"]):
        return "clip"
    if any(word in text for word in ["reaction", "pov", "funny", "sarcastic"]):
        return "gif"
    if any(word in text for word in ["emoji", "express", "mood"]):
        return "emoji"
    if any(word in text for word in ["sticker", "approval", "shocked"]):
        return "sticker"
    return "meme"


async def choose_media_type_with_groq(content: dict[str, Any], tone: str) -> dict[str, str]:
    key = os.getenv("GROQ_API_KEY")
    if not key:
        media_type = _fallback_media_type(content, tone)
        return {
            "media_type": media_type,
            "feeling": tone,
            "reason": "Fallback selector used because GROQ_API_KEY is missing.",
        }

    prompt = f"""
Choose the best KLIPY media type for this short-form content feeling.

Allowed media_type values:
- gif: reaction/motion moment
- meme: static meme/template
- sticker: expressive overlay or chat-style reaction
- clip: cinematic/video moment
- emoji: AI emoji/reaction symbol

Content:
Hook: {content.get("hook")}
Meme format: {content.get("meme_format")}
Caption: {content.get("caption")}
Query: {content.get("klipy_query")}
Tone: {tone}

Return JSON only:
{{"media_type":"gif|meme|sticker|clip|emoji","feeling":"short feeling label","reason":"short reason"}}
""".strip()

    try:
        import httpx

        async with httpx.AsyncClient(timeout=12) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                json={
                    "model": os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
                    "messages": [
                        {"role": "system", "content": "You choose media types for a social media content engine."},
                        {"role": "user", "content": prompt},
                    ],
                    "response_format": {"type": "json_object"},
                },
            )
            response.raise_for_status()
            payload = response.json()
        parsed = parse_json_object(payload["choices"][0]["message"]["content"])
        media_type = str(parsed.get("media_type", "")).lower()
        if media_type not in MEDIA_TYPES:
            media_type = _fallback_media_type(content, tone)
        return {
            "media_type": media_type,
            "feeling": str(parsed.get("feeling") or tone),
            "reason": str(parsed.get("reason") or "Selected by Groq."),
        }
    except Exception as exc:
        media_type = _fallback_media_type(content, tone)
        return {
            "media_type": media_type,
            "feeling": tone,
            "reason": f"Fallback selector used because {_safe_failure_reason('Groq media selection', exc)}",
        }
