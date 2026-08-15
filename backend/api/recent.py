"""
api/recent.py — Recent generations list endpoint.
"""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from database.database import get_db
from database.models import Generation
from schemas.recent import RecentGenerationItem, RecentGenerationsResponse
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/recent", tags=["Recent"])

_RECENT_LIMIT = 10


@router.get(
    "",
    response_model=RecentGenerationsResponse,
    summary="Get the latest content generations",
)
def get_recent_generations(db: Session = Depends(get_db)):
    """
    Return the 10 most recent content generations with a summary view.
    Includes hook, tone, and platform for quick display.
    """
    generations = (
        db.query(Generation)
        .options(joinedload(Generation.product))
        .order_by(Generation.created_at.desc())
        .limit(_RECENT_LIMIT)
        .all()
    )

    items: List[RecentGenerationItem] = []
    for gen in generations:
        resp = gen.response_dict
        hook = resp.get("hook", "—")
        tone = gen.product.tone if gen.product else "—"
        platform = gen.product.platform if gen.product else "—"

        items.append(
            RecentGenerationItem(
                id=gen.id,
                product_id=gen.product_id,
                hook=hook,
                tone=tone,
                platform=platform,
                created_at=gen.created_at,
            )
        )

    return RecentGenerationsResponse(items=items, total=len(items))
