from schemas.trends import ContentSuggestions, RankedTrend


def generate_trend_content(brand: str, industry: str, top_trends: list[RankedTrend]) -> ContentSuggestions:
    lead = top_trends[0] if top_trends else None
    trend_name = lead.title if lead else "the trend everyone is talking about"
    category = lead.analysis.trendCategory if lead else "viral"

    return ContentSuggestions(
        captions=[
            f"{brand} just found its {category} moment.",
            f"When {trend_name} meets {industry}, the scroll finally stops.",
            f"POV: {brand} turns a trend into something people actually save.",
        ],
        reelIdeas=[
            f"Open with the '{trend_name}' format, then reveal the product benefit in 3 seconds.",
            f"Use a before/after cut that connects {industry} pain points to {brand}.",
            "End with a comment-bait question that invites users to tag a friend.",
        ],
        hashtags=[
            f"#{brand.replace(' ', '')}",
            "#TrendPilotAI",
            "#ViralMarketing",
            "#MemeMarketing",
            f"#{industry.replace(' ', '').replace('&', 'And')}",
        ],
        cta=[
            "Comment your version of this trend.",
            "Tag someone who needs this.",
            "Save this idea before the trend peaks.",
        ],
    )
