from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


Platform = Literal["Instagram", "YouTube Shorts", "Both"]
Tone = Literal[
    "Funny",
    "Sarcastic",
    "Professional",
    "Emotional",
    "Luxury",
    "Gen-Z",
    "Educational",
    "Meme Style",
]


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    category: str = Field(..., min_length=1, max_length=80)
    description: str = Field(..., min_length=5, max_length=2000)
    features: str = ""
    problem: str = ""
    audience: str = Field(..., min_length=1, max_length=240)
    price_range: str = ""
    competitors: str = ""
    platform: Platform
    tone: Tone = "Funny"
    requirements: str = ""


class ProductResponse(BaseModel):
    product_id: int
    message: str


class ProductOut(ProductCreate):
    id: int
    created_at: datetime | str
