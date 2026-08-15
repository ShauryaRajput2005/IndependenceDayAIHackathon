import json

from fastapi import APIRouter

from database.database import fetch_all
from schemas.recent import RecentGeneration


router = APIRouter(prefix="/api/recent", tags=["recent"])


@router.get("", response_model=list[RecentGeneration])
def list_recent(limit: int = 10):
    rows = fetch_all(
        """
        SELECT generations.id AS generation_id,
               generations.product_id,
               products.name AS product_name,
               generations.tone,
               generations.response,
               generations.created_at
        FROM generations
        JOIN products ON products.id = generations.product_id
        ORDER BY generations.created_at DESC, generations.id DESC
        LIMIT ?
        """,
        (max(1, min(limit, 50)),),
    )
    return [
        {
            "generation_id": row["generation_id"],
            "product_id": row["product_id"],
            "product_name": row["product_name"],
            "tone": row["tone"],
            "response": json.loads(row["response"]),
            "created_at": row["created_at"],
        }
        for row in rows
    ]
