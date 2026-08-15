"""
schemas/product.py — Request and response schemas for the Product API.
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Product name")
    category: str = Field(..., min_length=1, max_length=100, description="Product category")
    description: str = Field(..., min_length=1, description="Product description")
    features: List[str] = Field(default_factory=list, description="Key product features")
    problem_solved: Optional[str] = Field(None, description="Core problem the product solves")
    target_audience: Optional[str] = Field(None, max_length=255)
    price: Optional[str] = Field(None, max_length=100)
    platform: str = Field(..., description="Target social platform (instagram, tiktok, youtube, twitter)")
    tone: str = Field(..., description="Content tone (funny, sarcastic, professional, etc.)")
    requirements: Optional[str] = Field(None, description="Free-text custom requirements")

    model_config = {"json_schema_extra": {
        "example": {
            "name": "AI Resume Builder",
            "category": "Education",
            "description": "AI tool that creates ATS-friendly resumes",
            "features": ["ATS optimization", "AI suggestions", "Resume templates"],
            "problem_solved": "Students struggle to create effective resumes",
            "target_audience": "Indian college students",
            "price": "Free",
            "platform": "instagram",
            "tone": "sarcastic",
            "requirements": "Make it Hinglish, funny and meme-heavy",
        }
    }}


class ProductCreateResponse(BaseModel):
    id: int
    message: str


class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    description: str
    features: List[str]
    problem_solved: Optional[str]
    target_audience: Optional[str]
    price: Optional[str]
    platform: str
    tone: str
    requirements: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}
