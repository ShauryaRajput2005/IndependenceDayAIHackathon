"""
schemas/feedback.py — Request and response schemas for the Feedback API.
"""
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

FEEDBACK_TYPES = Literal[
    "funnier",
    "more_trendy",
    "more_relatable",
    "more_professional",
    "better_hook",
    "shorter",
    "like",
    "dislike",
]


class FeedbackCreate(BaseModel):
    generation_id: int = Field(..., description="ID of the generation being rated")
    feedback_type: FEEDBACK_TYPES = Field(..., description="Predefined feedback category")
    comment: Optional[str] = Field(None, description="Optional free-text comment")

    model_config = {"json_schema_extra": {
        "example": {
            "generation_id": 42,
            "feedback_type": "funnier",
            "comment": "Make the dialogue more savage",
        }
    }}


class FeedbackResponse(BaseModel):
    id: int
    generation_id: int
    feedback_type: str
    comment: Optional[str]
    created_at: datetime
    preference_saved: bool = False

    model_config = {"from_attributes": True}
