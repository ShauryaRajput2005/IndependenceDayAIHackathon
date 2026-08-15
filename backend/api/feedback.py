from fastapi import APIRouter, HTTPException

from database.database import execute, fetch_one
from schemas.feedback import FeedbackCreate, FeedbackResponse
from services.memory_service import add_preference, feedback_to_preference


router = APIRouter(prefix="/api/feedback", tags=["feedback"])


@router.post("/create", response_model=FeedbackResponse)
def create_feedback(payload: FeedbackCreate):
    generation = fetch_one("SELECT * FROM generations WHERE id = ?", (payload.generation_id,))
    if not generation:
        raise HTTPException(status_code=404, detail="Generation not found")

    preference, preference_type = feedback_to_preference(payload.feedback)
    feedback_id = execute(
        """
        INSERT INTO feedback (generation_id, product_id, feedback, sentiment)
        VALUES (?, ?, ?, ?)
        """,
        (payload.generation_id, generation["product_id"], payload.feedback, payload.sentiment),
    )
    add_preference(generation["product_id"], preference, preference_type)

    return {
        "feedback_id": feedback_id,
        "preference": preference,
        "message": "Feedback saved and memory updated",
    }
