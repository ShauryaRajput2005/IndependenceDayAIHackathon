import asyncio

from schemas.trends import TrendItem, TrendSource
from services.klipy_service import get_trending_media


async def collect_trends(limit_per_type: int = 6) -> list[TrendSource]:
    media_types = ["gif", "meme", "sticker", "clip", "emoji"]
    results = await asyncio.gather(
        *(get_trending_media(media_type=media_type, limit=limit_per_type) for media_type in media_types)
    )

    klipy_trends = [
        TrendItem.model_validate(item)
        for media_items in results
        for item in media_items
    ]

    return [
        TrendSource(source="klipy", trends=klipy_trends),
        TrendSource(source="reddit_future", trends=[]),
        TrendSource(source="google_trends_future", trends=[]),
        TrendSource(source="youtube_shorts_future", trends=[]),
    ]
