"""
services/memory_service.py — Lightweight preference memory backed by SQLite.
"""
from typing import List, Tuple
from sqlalchemy.orm import Session

from database.models import Preference
from utils.logger import get_logger

logger = get_logger(__name__)


def get_preferences(db: Session, product_id: int) -> List[Preference]:
    """Return all stored preferences for a product."""
    return (
        db.query(Preference)
        .filter(Preference.product_id == product_id)
        .order_by(Preference.created_at.desc())
        .all()
    )


def add_preference(
    db: Session,
    product_id: int,
    preference: str,
    preference_type: str,  # "positive" | "negative"
) -> Preference:
    """
    Add a preference — skip if an identical one already exists for this product.
    """
    preference = preference.strip()
    existing = (
        db.query(Preference)
        .filter(
            Preference.product_id == product_id,
            Preference.preference == preference,
            Preference.type == preference_type,
        )
        .first()
    )
    if existing:
        logger.info("Preference already exists — skipping duplicate: %s", preference)
        return existing

    pref = Preference(
        product_id=product_id,
        preference=preference,
        type=preference_type,
    )
    db.add(pref)
    db.commit()
    db.refresh(pref)
    logger.info("Saved preference [%s]: %s (product_id=%d)", preference_type, preference, product_id)
    return pref


def build_memory_context(db: Session, product_id: int) -> str:
    """
    Build a human-readable preference block for injection into the prompt.
    Returns a string like:
        Positive preferences: sarcastic humor, Hinglish, short hooks
        Negative preferences: corporate language
    """
    prefs = get_preferences(db, product_id)
    if not prefs:
        return "No preferences recorded yet. Use your best judgment."

    positive = [p.preference for p in prefs if p.type == "positive"]
    negative = [p.preference for p in prefs if p.type == "negative"]

    parts = []
    if positive:
        parts.append("Things the user loves (do more of this):\n" + "\n".join(f"  + {p}" for p in positive))
    if negative:
        parts.append("Things the user dislikes (avoid these):\n" + "\n".join(f"  - {p}" for p in negative))

    return "\n\n".join(parts)
