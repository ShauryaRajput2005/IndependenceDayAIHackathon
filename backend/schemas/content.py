from typing import Any

from pydantic import BaseModel, Field


class ContentGenerateRequest(BaseModel):
    product_id: int = Field(..., gt=0)
    tone: str | None = None
    requirements: str | None = None


class Scene(BaseModel):
    scene: str
    time: str


class MemeAsset(BaseModel):
    title: str | None = None
    url: str | None = None
    preview: str | None = None
    source: str = "fallback"


class GeneratedContent(BaseModel):
    hook: str
    meme_format: str
    dialogue: list[str]
    script: list[Scene]
    caption: str
    klipy_query: str
    hashtags: list[str] = []
    viral_score: int = Field(default=78, ge=0, le=100)
    trend: dict[str, Any] | None = None
    meme: MemeAsset | None = None


class ContentGenerateResponse(GeneratedContent):
    generation_id: int
    product_id: int
