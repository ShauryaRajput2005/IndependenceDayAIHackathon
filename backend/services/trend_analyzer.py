from schemas.trends import TrendAnalysis, TrendItem


def _contains_any(text: str, words: list[str]) -> bool:
    lowered = text.lower()
    return any(word.lower() in lowered for word in words if word)


def analyze_trend(brand: str, industry: str, audience: str, trend: TrendItem) -> TrendAnalysis:
    text = " ".join([trend.title, trend.mediaType, *trend.tags]).lower()
    industry_words = [word for word in industry.replace("&", " ").replace("/", " ").split() if len(word) > 2]
    brand_words = [word for word in brand.split() if len(word) > 2]

    engagement = min(100, ((trend.likes or 0) / 1500) + ((trend.shares or 0) / 800) + ((trend.views or 0) / 12000))
    relevance = 58
    if _contains_any(text, industry_words):
        relevance += 18
    if _contains_any(text, brand_words):
        relevance += 10
    if trend.mediaType in {"meme", "gif", "clip"}:
        relevance += 8

    viral_potential = min(100, 50 + engagement * 0.35 + len(trend.tags) * 2)
    freshness = trend.freshness

    category = "nostalgia" if _contains_any(text, ["school", "childhood", "old", "lunch"]) else "reaction"
    if _contains_any(text, ["before", "after", "transformation", "reveal"]):
        category = "transformation"
    if _contains_any(text, ["starter", "pov", "main"]):
        category = "relatable"

    recommended_type = trend.mediaType
    reason = f"Strong {category} fit with {audience} and reusable {trend.mediaType} format."
    trend_score = round(viral_potential * 0.35 + relevance * 0.30 + engagement * 0.20 + freshness * 0.15)

    return TrendAnalysis(
        trendId=trend.id,
        trendScore=max(0, min(100, trend_score)),
        trendCategory=category,
        audience=audience,
        recommendedMediaType=recommended_type,
        reason=reason,
        viralPotential=max(0, min(100, viral_potential)),
        relevance=max(0, min(100, relevance)),
        engagement=max(0, min(100, engagement)),
        freshness=max(0, min(100, freshness)),
    )


def analyze_trends(brand: str, industry: str, audience: str, trends: list[TrendItem]) -> list[TrendAnalysis]:
    return [analyze_trend(brand, industry, audience, trend) for trend in trends]
