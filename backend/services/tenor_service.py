"""
services/tenor_service.py — Klipy GIF/meme search service (Tenor drop-in replacement).

Klipy is a modern GIF/meme API explicitly designed as a migration target from Tenor.
Base URL: https://api.klipy.com
Endpoint: GET /api/v1/{API_KEY}/gifs/search

If KLIPY_API_KEY is missing or the request fails, generation continues normally.
"""
from typing import Optional

import httpx

from config import get_settings
from schemas.content import GifResult
from utils.logger import get_logger

logger = get_logger(__name__)

KLIPY_SEARCH_URL = "https://api.klipy.com/api/v1/{api_key}/gifs/search"
_RESULT_LIMIT = 5


def _parse_gif_result(item: dict) -> Optional[GifResult]:
    """
    Normalise a single Klipy result item into our GifResult schema.
    Prefer tinygif → mediumgif → gif for previews (smallest first).
    """
    try:
        media_formats = item.get("media_formats", {}) or item.get("media", {})

        preview = (
            media_formats.get("tinygif")
            or media_formats.get("nanogif")
            or media_formats.get("mediumgif")
            or media_formats.get("gif")
        )
        full = media_formats.get("gif") or preview

        if not preview or not full:
            return None

        preview_url = preview.get("url", "") if isinstance(preview, dict) else str(preview)
        full_url = full.get("url", "") if isinstance(full, dict) else str(full)
        dims = full.get("dims", [None, None]) if isinstance(full, dict) else [None, None]

        return GifResult(
            id=str(item.get("id", "")),
            title=item.get("title", item.get("content_description", "")),
            preview_url=preview_url,
            gif_url=full_url,
            width=dims[0] if dims else None,
            height=dims[1] if dims else None,
        )
    except Exception as exc:
        logger.warning("Failed to parse Klipy result item: %s", exc)
        return None


async def search_gif(query: str) -> Optional[GifResult]:
    """
    Search Klipy for a GIF matching the query.
    Returns the best result or None on any failure / missing key.
    Generation NEVER fails because of this function.
    """
    settings = get_settings()
    api_key = getattr(settings, "klipy_api_key", "") or settings.tenor_api_key

    if not api_key:
        logger.info("Klipy API key not configured — skipping GIF search.")
        return None

    url = KLIPY_SEARCH_URL.format(api_key=api_key)
    params = {
        "q": query,
        "limit": _RESULT_LIMIT,
        "media_filter": "tinygif,gif",
        "contentfilter": "low",
    }

    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

        # Klipy wraps results in either 'results' or 'data'
        results = data.get("results") or data.get("data") or []
        if not results:
            logger.info("Klipy returned no results for query: %s", query)
            return None

        for item in results:
            parsed = _parse_gif_result(item)
            if parsed:
                logger.info("Klipy GIF found for query '%s': %s", query, parsed.id)
                return parsed

        return None

    except httpx.HTTPStatusError as exc:
        logger.warning(
            "Klipy HTTP error %s for query '%s': %s",
            exc.response.status_code,
            query,
            exc,
        )
        return None
    except httpx.RequestError as exc:
        logger.warning("Klipy request error for query '%s': %s", query, exc)
        return None
    except Exception as exc:
        logger.error("Unexpected Klipy error for query '%s': %s", query, exc)
        return None
