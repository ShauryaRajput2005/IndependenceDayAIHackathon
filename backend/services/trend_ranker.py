from schemas.trends import RankedTrend, TrendAnalysis, TrendItem


def rank_trends(trends: list[TrendItem], analyses: list[TrendAnalysis], limit: int = 10) -> list[RankedTrend]:
    analysis_by_id = {analysis.trendId: analysis for analysis in analyses}
    ranked: list[RankedTrend] = []

    for trend in trends:
        analysis = analysis_by_id[trend.id]
        score = (
            analysis.viralPotential * 0.35
            + analysis.relevance * 0.30
            + analysis.engagement * 0.20
            + analysis.freshness * 0.15
        )
        ranked.append(
            RankedTrend(
                **trend.model_dump(),
                score=round(score, 2),
                analysis=analysis,
            )
        )

    return sorted(ranked, key=lambda item: item.score, reverse=True)[:limit]
