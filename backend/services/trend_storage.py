import json

from database.database import execute
from schemas.trends import RankedTrend, TrendAnalyzeResponse, TrendItem, TrendPrediction


def store_snapshots(trends: list[TrendItem]) -> None:
    for trend in trends:
        execute(
            """
            INSERT INTO trend_snapshots (source, media_type, title, tags, url, metrics)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                trend.source,
                trend.mediaType,
                trend.title,
                json.dumps(trend.tags),
                trend.url or "",
                json.dumps(
                    {
                        "views": trend.views,
                        "shares": trend.shares,
                        "likes": trend.likes,
                        "freshness": trend.freshness,
                    }
                ),
            ),
        )


def store_analysis(brand: str, industry: str, response: TrendAnalyzeResponse) -> None:
    execute(
        """
        INSERT INTO trend_analyses (brand, industry, response)
        VALUES (?, ?, ?)
        """,
        (brand, industry, response.model_dump_json()),
    )


def store_predictions(brand: str, industry: str, predictions: list[TrendPrediction]) -> None:
    for prediction in predictions:
        execute(
            """
            INSERT INTO trend_predictions (brand, industry, prediction, confidence)
            VALUES (?, ?, ?, ?)
            """,
            (brand, industry, prediction.model_dump_json(), prediction.confidence),
        )
