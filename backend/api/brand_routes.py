from fastapi import APIRouter, HTTPException

from database.database import fetch_all, fetch_one
from services.memory_service import get_memory


router = APIRouter(prefix="/api/brand", tags=["brand"])


@router.get("/{product_id}")
def get_brand_context(product_id: int):
    product = fetch_one("SELECT * FROM products WHERE id = ?", (product_id,))
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    generations = fetch_all(
        """
        SELECT id, tone, created_at
        FROM generations
        WHERE product_id = ?
        ORDER BY created_at DESC
        LIMIT 5
        """,
        (product_id,),
    )
    return {
        "product": dict(product),
        "memory": get_memory(product_id),
        "recent_generations": [dict(row) for row in generations],
    }
