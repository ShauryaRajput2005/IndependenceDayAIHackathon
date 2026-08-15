from pydantic import BaseModel, Field


class FeedbackCreate(BaseModel):
    generation_id: int = Field(..., gt=0)
    feedback: str = Field(..., min_length=1, max_length=1000)
    sentiment: str = "Positive"


class FeedbackResponse(BaseModel):
    feedback_id: int
    preference: str
    message: str
