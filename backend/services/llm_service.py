import os
from sqlite3 import Row
from typing import Any

from prompts.system import SYSTEM_PROMPT
from utils.json_parser import parse_json_object


def _fallback_content(product: Row, tone: str) -> dict[str, Any]:
    audience = product["audience"]
    product_name = product["name"]
    category = product["category"]
    platform = product["platform"]
    meme_format = "POV Meme" if tone in {"Funny", "Gen-Z", "Meme Style", "Sarcastic"} else "Expectation vs Reality"
    query = f"{audience} {category} funny reaction"

    return {
        "hook": f"POV: {audience} discover {product_name} exactly when they need it",
        "meme_format": meme_format,
        "dialogue": [
            f"Bro, why is {category.lower()} still this stressful?",
            f"Relax. {product_name} just handled the annoying part.",
        ],
        "script": [
            {"scene": "Open on the audience stuck in the old frustrating routine.", "time": "0-3 sec"},
            {"scene": f"Show {product_name} solving the pain point in one clean moment.", "time": "3-8 sec"},
            {"scene": f"Cut to a punchline that feels native to {platform}.", "time": "8-15 sec"},
        ],
        "caption": f"{product_name} for anyone tired of doing it the hard way.",
        "klipy_query": query,
        "hashtags": ["#TrendPilot", "#StartupMarketing", "#ShortFormContent"],
        "viral_score": 76,
    }


async def _post_json(url: str, headers: dict[str, str], payload: dict[str, Any]) -> str:
    import httpx

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
    return str(data)


async def _call_gemini(prompt: str) -> dict[str, Any] | None:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
    payload = {
        "contents": [{"parts": [{"text": f"{SYSTEM_PROMPT}\n\n{prompt}"}]}],
        "generationConfig": {"response_mime_type": "application/json"},
    }
    try:
        import httpx

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        return parse_json_object(text)
    except Exception:
        return None


async def _call_openai_compatible(prompt: str, provider: str) -> dict[str, Any] | None:
    config = {
        "openrouter": {
            "key": os.getenv("OPENROUTER_API_KEY"),
            "url": "https://openrouter.ai/api/v1/chat/completions",
            "model": os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
        },
        "groq": {
            "key": os.getenv("GROQ_API_KEY"),
            "url": "https://api.groq.com/openai/v1/chat/completions",
            "model": os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        },
    }[provider]
    if not config["key"]:
        return None

    headers = {"Authorization": f"Bearer {config['key']}", "Content-Type": "application/json"}
    payload = {
        "model": config["model"],
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "response_format": {"type": "json_object"},
    }

    try:
        import httpx

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(config["url"], headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
        return parse_json_object(data["choices"][0]["message"]["content"])
    except Exception:
        return None


async def generate_content(product: Row, prompt: str, tone: str) -> dict[str, Any]:
    for provider_call in (
        lambda: _call_gemini(prompt),
        lambda: _call_openai_compatible(prompt, "openrouter"),
        lambda: _call_openai_compatible(prompt, "groq"),
    ):
        result = await provider_call()
        if result:
            return result
    return _fallback_content(product, tone)
