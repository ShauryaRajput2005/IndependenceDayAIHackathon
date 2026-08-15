import asyncio
import hashlib
import os
import time
from typing import Any


KLIPY_BASE_URL = "https://api.klipy.com/v2"
MEDIA_FILTERS = {
    "gif": "gif,mediumgif,tinygif,nanogif,preview",
    "meme": "gif,mediumgif,tinygif,nanogif,preview",
    "sticker": "gif,mediumgif,tinygif,nanogif,preview",
    "clip": "mp4,tinymp4,gif,mediumgif,tinygif,nanogif,preview",
    "emoji": "gif,mediumgif,tinygif,nanogif,preview",
}

_last_request_at = 0.0
_last_provider_status = "not_requested"


def _fallback_trends(media_type: str, limit: int = 10, reason: str | None = None) -> list[dict[str, Any]]:
    seeds = {
        "gif": ["POV reaction", "main character moment", "awkward silence"],
        "meme": ["school lunch nostalgia", "expectation vs reality", "starter pack"],
        "sticker": ["shocked sticker", "approval reaction", "facepalm sticker"],
        "clip": ["quick transformation", "before after reveal", "dramatic entrance"],
        "emoji": ["cry laugh", "skull reaction", "sparkle approval"],
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


def _media_url(media: dict[str, Any]) -> tuple[str | None, str | None]:
    formats = media.get("media_formats") or media.get("mediaFormats") or {}
    for key in ("gif", "mp4", "mediumgif", "tinygif", "tinymp4", "nanogif", "preview"):
        item = formats.get(key) or {}
        if item.get("url"):
            preview = (formats.get("preview") or formats.get("tinygif") or formats.get("nanogif") or item).get("url")
            return item.get("url"), preview
    return media.get("url"), media.get("preview")


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

    params = {"key": api_key, **params}
    for attempt in range(retries + 1):
        try:
            import httpx

            await _rate_limit()
            async with httpx.AsyncClient(timeout=3) as client:
                response = await client.get(f"{KLIPY_BASE_URL}{path}", params=params)
                response.raise_for_status()
                _last_provider_status = "klipy_ok"
                return response.json()
        except ImportError:
            _last_provider_status = "missing_httpx_dependency"
            return None
        except Exception:
            if attempt >= retries:
                _last_provider_status = "klipy_request_failed"
                return None
            await asyncio.sleep(0.2 * (attempt + 1))
    return None


async def search_klipy_media(query: str, media_type: str = "gif", limit: int = 10, page: int = 1) -> list[dict[str, Any]]:
    params = {
        "q": query,
        "limit": limit,
        "pos": max(0, page - 1) * limit,
        "media_filter": MEDIA_FILTERS.get(media_type, "gif,tinygif"),
        "contentfilter": "medium",
    }
    payload = await _request_klipy("/search", params)
    results = (payload or {}).get("results") or []
    if not results:
        return _fallback_trends(media_type, limit, "klipy_empty" if payload else _last_provider_status)
    return [_normalize_media_item(item, media_type, index) for index, item in enumerate(results[:limit], start=1)]


async def get_trending_media(media_type: str = "gif", limit: int = 10, page: int = 1) -> list[dict[str, Any]]:
    params = {
        "q": f"trending {media_type}",
        "limit": limit,
        "pos": max(0, page - 1) * limit,
        "media_filter": MEDIA_FILTERS.get(media_type, "gif,tinygif"),
        "contentfilter": "medium",
    }
    payload = await _request_klipy("/search", params)
    results = (payload or {}).get("results") or []
    if not results:
        return _fallback_trends(media_type, limit, "klipy_empty" if payload else _last_provider_status)
    return [_normalize_media_item(item, media_type, index) for index, item in enumerate(results[:limit], start=1)]


async def fetch_klipy_meme(query: str) -> dict[str, Any]:
    results = await search_klipy_media(query=query, media_type="meme", limit=1)
    first = results[0] if results else _fallback_trends("meme", 1)[0]
    return {
        "title": first["title"],
        "url": first.get("url"),
        "preview": first.get("preview"),
        "source": first["source"] if first["source"] == "klipy" else "fallback",
    }
