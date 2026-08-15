import asyncio

from schemas.trends import MediaSuggestions, RankedTrend, TrendItem
from services.klipy_service import search_klipy_media


async def recommend_media(brand: str, top_trend: RankedTrend | None) -> MediaSuggestions:
    if not top_trend:
        return MediaSuggestions()

    keyword = " ".join([brand, top_trend.title, *top_trend.tags[:4]])
    memes, gifs, clips, stickers, emojis = await asyncio.gather(
        search_klipy_media(keyword, media_type="meme", limit=3),
        search_klipy_media(keyword, media_type="gif", limit=3),
        search_klipy_media(keyword, media_type="clip", limit=3),
        search_klipy_media(keyword, media_type="sticker", limit=3),
        search_klipy_media(keyword, media_type="emoji", limit=3),
    )

    return MediaSuggestions(
        recommendedMemes=[TrendItem.model_validate(item) for item in memes],
        recommendedGifs=[TrendItem.model_validate(item) for item in gifs],
        recommendedClips=[TrendItem.model_validate(item) for item in clips],
        recommendedStickers=[TrendItem.model_validate(item) for item in stickers],
        recommendedEmojis=[TrendItem.model_validate(item) for item in emojis],
    )
