"""
api/feedback.py — Feedback submission endpoint with preference learning.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Feedback, Generation
from schemas.feedback import FeedbackCreate, FeedbackResponse
from services import memory_service
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/feedback", tags=["Feedback"])

# Deterministic preference map — no LLM call needed for known feedback types
FEEDBACK_PREFERENCE_MAP: dict = {
    "funnier": ("positive", "humorous, punchy, and sarcastic content"),
    "more_trendy": ("positive", "trend-native formats and current internet culture references"),
    "more_relatable": ("positive", "relatable storytelling and audience-specific scenarios"),
    "more_professional": ("positive", "professional and polished tone"),
    "better_hook": ("positive", "stronger curiosity-building opening hooks"),
    "shorter": ("positive", "concise and punchy scripts under 30 seconds"),
    "like": ("positive", "current style and creative direction"),
    "dislike": ("negative", "current style and creative direction"),
}


@router.post(
    "",
    response_model=FeedbackResponse,
    summary="Submit feedback on a generation",
    status_code=201,
)
def submit_feedback(payload: FeedbackCreate, db: Session = Depends(get_db)):
    """
    Submit feedback for a content generation.

    For known feedback types, preferences are saved immediately without an LLM call.
    For free-text comments on unknown types (future extension), an LLM call would
    extract a preference — but this is not needed for the current feedback_type set.
    """
    # ── Validate generation exists ─────────────────────────────────────────────
    generation: Generation = (
        db.query(Generation)
        .filter(Generation.id == payload.generation_id)
        .first()
    )
    if not generation:
        raise HTTPException(
            status_code=404,
            detail=f"Generation {payload.generation_id} not found",
        )

    # ── Save feedback record ───────────────────────────────────────────────────
    feedback = Feedback(
        generation_id=payload.generation_id,
        feedback_type=payload.feedback_type,
        comment=payload.comment,
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    logger.info(
        "Feedback saved: id=%d generation_id=%d type='%s'",
        feedback.id,
        payload.generation_id,
        payload.feedback_type,
    )

    # ── Interpret and save preference ──────────────────────────────────────────
    preference_saved = False
    if payload.feedback_type in FEEDBACK_PREFERENCE_MAP:
        pref_type, pref_text = FEEDBACK_PREFERENCE_MAP[payload.feedback_type]

        # Enrich with comment context if provided
        if payload.comment and payload.feedback_type not in ("like", "dislike"):
            pref_text = f"{pref_text} (user note: {payload.comment[:80]})"

        memory_service.add_preference(
            db=db,
            product_id=generation.product_id,
            preference=pref_text,
            preference_type=pref_type,
        )
        preference_saved = True

    return FeedbackResponse(
        id=feedback.id,
        generation_id=feedback.generation_id,
        feedback_type=feedback.feedback_type,
        comment=feedback.comment,
        created_at=feedback.created_at,
        preference_saved=preference_saved,
    )
