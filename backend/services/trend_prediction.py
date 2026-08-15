from collections import Counter

from schemas.trends import RankedTrend, TrendPrediction


def predict_trends(top_trends: list[RankedTrend]) -> list[TrendPrediction]:
    if not top_trends:
        return [
            TrendPrediction(
                futureTrend="relatable reaction content",
                confidence=0.62,
                growthPrediction="+18%",
                basis="Fallback based on durable short-form formats.",
            )
        ]

    categories = Counter(trend.analysis.trendCategory for trend in top_trends)
    media_types = Counter(trend.mediaType for trend in top_trends)
    category, category_count = categories.most_common(1)[0]
    media_type, _ = media_types.most_common(1)[0]
    avg_score = sum(trend.score for trend in top_trends[:5]) / min(5, len(top_trends))

    return [
        TrendPrediction(
            futureTrend=f"{category} {media_type} content",
            confidence=round(min(0.94, 0.55 + avg_score / 250), 2),
            growthPrediction=f"+{round(18 + avg_score / 3)}%",
            basis="Predicted from score concentration, engagement velocity, and recurring format frequency.",
        ),
        TrendPrediction(
            futureTrend=f"{top_trends[0].title} remixes",
            confidence=round(min(0.9, 0.5 + category_count / 10), 2),
            growthPrediction=f"+{round(12 + top_trends[0].analysis.viralPotential / 4)}%",
            basis="Top trend has strong viral potential and reusable tags.",
        ),
    ]
