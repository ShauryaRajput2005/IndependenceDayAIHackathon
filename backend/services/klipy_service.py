import asyncio
import hashlib
import os
import time
from typing import Any


KLIPY_BASE_URL = "https://api.klipy.com/api/v1"
TRENDING_PATHS = {
    "gif": "gifs/trending",
    "meme": "static-memes/trending",
    "sticker": "stickers/trending",
    "clip": "clips/trending",
    "emoji": "emojis/trending",
}

_last_request_at = 0.0
_last_provider_status = "not_requested"


def _stable_index(text: str, modulo: int, salt: str = "") -> int:
    if modulo <= 1:
        return 0
    digest = hashlib.sha256(f"{text}:{salt}".encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % modulo


def _provider_failure_status(error: Exception) -> str:
    response = getattr(error, "response", None)
    status_code = getattr(response, "status_code", None)
    if status_code:
        return f"klipy_http_{status_code}"
    return f"klipy_{error.__class__.__name__.lower()}"


def _fallback_trends(media_type: str, limit: int = 10, reason: str | None = None) -> list[dict[str, Any]]:
    seeds = {
        "gif": [
            "POV reaction",
            "main character moment",
            "awkward silence",
            "instant regret",
            "happy dance",
            "side eye reaction",
            "dramatic gasp",
            "relatable chaos",
        ],
        "meme": [
            "school lunch nostalgia",
            "expectation vs reality",
            "starter pack",
            "exam panic",
            "luxury premium taste meme",
            "before after glow up",
            "that one friend",
            "weekend mood",
        ],
        "sticker": [
            "shocked sticker",
            "approval reaction",
            "facepalm sticker",
            "tiny celebration",
            "confused mood",
            "verified vibe",
            "no way reaction",
            "soft flex",
        ],
        "clip": [
            "quick transformation",
            "before after reveal",
            "dramatic entrance",
            "cinematic product moment",
            "morning routine",
            "outfit reveal",
            "creator reaction",
            "street style shot",
        ],
        "emoji": [
            "cry laugh",
            "skull reaction",
            "sparkle approval",
            "fire mood",
            "mind blown",
            "heart eyes",
            "panic face",
            "clean check",
        ],
    }.get(media_type, ["viral reaction"])

    trends = []
    for index, title in enumerate(seeds[:limit], start=1):
        trends.append(
            {
                "id": f"fallback-{media_type}-{index}",
                "title": title,
                "mediaType": media_type,
                "source": "klipy_fallback",
                "views": 120000 - index * 7000,
                "shares": 9000 - index * 500,
                "likes": 24000 - index * 1200,
                "tags": title.split() + [media_type, "trend"],
                "url": None,
                "preview": None,
                "freshness": max(60, 96 - index * 6),
                "providerStatus": reason or _last_provider_status,
            }
        )
    return trends


def _rotate_results(results: list[dict[str, Any]], query: str, salt: str = "") -> list[dict[str, Any]]:
    if not results:
        return results
    start = _stable_index(query, len(results), salt)
    return results[start:] + results[:start]


def _rank_results_for_query(results: list[dict[str, Any]], query: str, salt: str = "") -> list[dict[str, Any]]:
    rotated = _rotate_results(results, query, salt)
    tokens = {token for token in query.lower().replace("#", " ").split() if len(token) > 2}
    if not tokens:
        return rotated

    def score(item: dict[str, Any]) -> int:
        haystack = " ".join(
            [
                str(item.get("title", "")),
                " ".join(str(tag) for tag in item.get("tags", [])),
            ]
        ).lower()
        return sum(1 for token in tokens if token in haystack)

    if not any(score(item) for item in rotated):
        return rotated
    return sorted(rotated, key=score, reverse=True)


def _find_url(value: Any) -> str | None:
    if isinstance(value, str) and value.startswith("http"):
        return value
    if isinstance(value, dict):
        if isinstance(value.get("url"), str) and value["url"].startswith("http"):
            return value["url"]
        for item in value.values():
            found = _find_url(item)
            if found:
                return found
    if isinstance(value, list):
        for item in value:
            found = _find_url(item)
            if found:
                return found
    return None


def _media_url(media: dict[str, Any]) -> tuple[str | None, str | None]:
    formats = media.get("media_formats") or media.get("mediaFormats") or {}
    for key in ("gif", "mp4", "mediumgif", "tinygif", "tinymp4", "nanogif", "preview"):
        item = formats.get(key) or {}
        if item.get("url"):
            preview = (formats.get("preview") or formats.get("tinygif") or formats.get("nanogif") or item).get("url")
            return item.get("url"), preview
    for key in ("url", "gif_url", "media_url", "image_url", "file", "src"):
        found = _find_url(media.get(key))
        if found:
            preview = _find_url(media.get("preview")) or _find_url(media.get("thumbnail")) or _find_url(media.get("thumb")) or found
            return found, preview
    images = media.get("images") or media.get("image") or {}
    if isinstance(images, dict):
        for key in ("original", "fixed_height", "preview", "downsized", "thumbnail"):
            item = images.get(key) or {}
            if isinstance(item, dict) and item.get("url"):
                return item.get("url"), (images.get("preview") or images.get("thumbnail") or item).get("url")
            if isinstance(item, str):
                return item, item
    found = _find_url(media)
    return found, found


def _metric_from_text(text: str, salt: str, floor: int, ceiling: int) -> int:
    digest = hashlib.sha256(f"{text}:{salt}".encode("utf-8")).hexdigest()
    return floor + int(digest[:8], 16) % max(1, ceiling - floor)


def _normalize_media_item(item: dict[str, Any], media_type: str, index: int) -> dict[str, Any]:
    title = item.get("content_description") or item.get("title") or item.get("name") or f"{media_type} trend {index}"
    url, preview = _media_url(item)
    raw_tags = item.get("tags") or item.get("keywords") or []
    tags = [str(tag).strip().lower() for tag in raw_tags if str(tag).strip()]
    if not tags:
        tags = [word.lower() for word in str(title).replace("#", "").split()[:6]]

    return {
        "id": str(item.get("id") or item.get("itemurl") or f"klipy-{media_type}-{index}"),
        "title": str(title),
        "mediaType": media_type,
        "source": "klipy",
        "views": item.get("views") or _metric_from_text(str(title), "views", 20000, 500000),
        "shares": item.get("shares") or _metric_from_text(str(title), "shares", 1000, 40000),
        "likes": item.get("likes") or _metric_from_text(str(title), "likes", 5000, 120000),
        "tags": tags,
        "url": url,
        "preview": preview,
        "freshness": min(100, 65 + index * 3),
        "providerStatus": _last_provider_status,
    }


async def _rate_limit() -> None:
    global _last_request_at
    elapsed = time.monotonic() - _last_request_at
    if elapsed < 0.15:
        await asyncio.sleep(0.15 - elapsed)
    _last_request_at = time.monotonic()


async def _request_klipy(path: str, params: dict[str, Any], retries: int = 1) -> dict[str, Any] | None:
    global _last_provider_status
    api_key = os.getenv("KLIPY_API_KEY")
    if not api_key:
        _last_provider_status = "missing_klipy_api_key"
        return None

    for attempt in range(retries + 1):
        try:
            import httpx

            await _rate_limit()
            async with httpx.AsyncClient(timeout=12) as client:
                response = await client.get(f"{KLIPY_BASE_URL}/{api_key}/{path}", params=params)
                response.raise_for_status()
                _last_provider_status = "klipy_ok"
                return response.json()
        except ImportError:
            _last_provider_status = "missing_httpx_dependency"
            return None
        except Exception as exc:
            if attempt >= retries:
                _last_provider_status = _provider_failure_status(exc)
                return None
            await asyncio.sleep(0.2 * (attempt + 1))
    return None


async def search_klipy_media(query: str, media_type: str = "gif", limit: int = 10, page: int = 1) -> list[dict[str, Any]]:
    requested_page = page or (_stable_index(query, 5, media_type) + 1)
    pool = []
    for offset in range(3):
        pool.extend(await get_trending_media(media_type=media_type, limit=max(limit, 12), page=requested_page + offset))
    return _rank_results_for_query(pool, query, media_type)[:limit]


async def get_trending_media(media_type: str = "gif", limit: int = 10, page: int = 1) -> list[dict[str, Any]]:
    path = TRENDING_PATHS.get(media_type, TRENDING_PATHS["gif"])
    params = {
        "page": max(1, page),
        "per_page": limit,
        "customer_id": os.getenv("KLIPY_CUSTOMER_ID", "trendpilot-user"),
        "locale": os.getenv("KLIPY_LOCALE", "en"),
        "content_filter": os.getenv("KLIPY_CONTENT_FILTER", "medium"),
    }
    payload = await _request_klipy(path, params)
    results = _extract_results(payload or {})
    if not results:
        return _fallback_trends(media_type, limit, "klipy_empty" if payload else _last_provider_status)
    return [_normalize_media_item(item, media_type, index) for index, item in enumerate(results[:limit], start=1)]


def _extract_results(payload: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("data", "results", "items", "gifs", "stickers", "clips", "emojis", "memes"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
        if isinstance(value, dict):
            for nested_key in ("data", "results", "items"):
                nested = value.get(nested_key)
                if isinstance(nested, list):
                    return nested
    return []


async def fetch_klipy_media(query: str, media_type: str = "meme") -> dict[str, Any]:
    results = await search_klipy_media(query=query, media_type=media_type, limit=1, page=0)
    first = results[0] if results else _fallback_trends(media_type, 1)[0]
    return {
        "title": first["title"],
        "url": first.get("url"),
        "preview": first.get("preview"),
        "source": first["source"] if first["source"] == "klipy" else "fallback",
        "mediaType": media_type,
        "providerStatus": first.get("providerStatus"),
    }


async def fetch_klipy_meme(query: str) -> dict[str, Any]:
    return await fetch_klipy_media(query=query, media_type="meme")
