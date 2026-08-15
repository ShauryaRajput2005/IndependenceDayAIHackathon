"""
services/tenor_service.py — Optional Tenor GIF search with graceful fallback.

Tenor's new API client registrations are closed as of Jan 2026.
If TENOR_API_KEY is absent or the request fails, generation continues normally.
"""
from typing import Optional

import httpx

from config import get_settings
from schemas.content import GifResult
from utils.logger import get_logger

logger = get_logger(__name__)

TENOR_SEARCH_URL = "https://tenor.googleapis.com/v2/search"
_RESULT_LIMIT = 5


def _parse_gif_result(item: dict) -> Optional[GifResult]:
    """
    Normalise a single Tenor result item into our GifResult schema.
    Prefer tinygif for previews; fall back to gif.
    """
    try:
        media_formats = item.get("media_formats", {})
        # Prefer smaller preview formats for faster loading
        preview = (
            media_formats.get("tinygif")
            or media_formats.get("mediumgif")
            or media_formats.get("gif")
        )
        full = media_formats.get("gif") or preview

        if not preview or not full:
            return None

        return GifResult(
            id=str(item.get("id", "")),
            title=item.get("title", ""),
            preview_url=preview.get("url", ""),
            gif_url=full.get("url", ""),
            width=full.get("dims", [None, None])[0],
            height=full.get("dims", [None, None])[1],
        )
    except Exception as exc:
        logger.warning("Failed to parse Tenor result item: %s", exc)
        return None


async def search_gif(query: str) -> Optional[GifResult]:
    """
    Search Tenor for a GIF matching the query.
    Returns the best result or None on any failure / missing key.
    """
    settings = get_settings()

    if not settings.tenor_api_key:
        logger.info("Tenor API key not configured — skipping GIF search.")
        return None

    params = {
        "q": query,
        "key": settings.tenor_api_key,
        "client_key": settings.tenor_client_key,
        "limit": _RESULT_LIMIT,
        "media_filter": "tinygif,gif",
    }

    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.get(TENOR_SEARCH_URL, params=params)
            response.raise_for_status()
            data = response.json()

        results = data.get("results", [])
        if not results:
            logger.info("Tenor returned no results for query: %s", query)
            return None

        # Return first successfully parsed result
        for item in results:
            parsed = _parse_gif_result(item)
            if parsed:
                return parsed

        return None

    except httpx.HTTPStatusError as exc:
        logger.warning("Tenor HTTP error %s for query '%s': %s", exc.response.status_code, query, exc)
        return None
    except httpx.RequestError as exc:
        logger.warning("Tenor request error for query '%s': %s", query, exc)
        return None
    except Exception as exc:
        logger.error("Unexpected Tenor error: %s", exc)
        return None
