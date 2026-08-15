import logging
import time

from schemas.trends import TrendAnalyzeRequest, TrendAnalyzeResponse, TrendItem
from services.cache_service import get_cache, set_cache
from services.content_suggestion_service import generate_trend_content
from services.media_recommendation import recommend_media
from services.trend_analyzer import analyze_trends
from services.trend_collector import collect_trends
from services.trend_prediction import predict_trends
from services.trend_ranker import rank_trends
from services.trend_storage import store_analysis, store_predictions, store_snapshots


logger = logging.getLogger("trendpilot.trends")


async def analyze_brand_trends(payload: TrendAnalyzeRequest) -> TrendAnalyzeResponse:
    started = time.perf_counter()
    cache_key = f"trend-analysis:{payload.brand.lower()}:{payload.industry.lower()}:{payload.audience.lower()}:{payload.limit}"
    cached = get_cache(cache_key)
    if cached:
        return TrendAnalyzeResponse.model_validate(cached)

    sources = await collect_trends(limit_per_type=max(3, min(8, payload.limit)))
    all_trends: list[TrendItem] = [trend for source in sources for trend in source.trends]
    store_snapshots(all_trends)

    analyses = analyze_trends(payload.brand, payload.industry, payload.audience, all_trends)
    top_trends = rank_trends(all_trends, analyses, limit=payload.limit)
    predictions = predict_trends(top_trends)
    media_suggestions = await recommend_media(payload.brand, top_trends[0] if top_trends else None)
    content = generate_trend_content(payload.brand, payload.industry, top_trends)

    latency_ms = round((time.perf_counter() - started) * 1000)
    response = TrendAnalyzeResponse(
        topTrends=top_trends,
        predictions=predictions,
        mediaSuggestions=media_suggestions,
        captions=content.captions,
        reelIdeas=content.reelIdeas,
        hashtags=content.hashtags,
        cta=content.cta,
        sources=sources,
        latencyMs=latency_ms,
    )

    store_predictions(payload.brand, payload.industry, predictions)
    store_analysis(payload.brand, payload.industry, response)
    set_cache(cache_key, response.model_dump(), ttl_seconds=900)
    logger.info("trend_analysis_completed brand=%s industry=%s latency_ms=%s", payload.brand, payload.industry, latency_ms)
    return response
