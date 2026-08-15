"""
schemas/content.py — AI output schema and content generation request/response.
"""
from typing import List, Optional

from pydantic import BaseModel, Field


# ── AI structured output schema (sent to Gemini as response_schema) ──────────

class TrendInfo(BaseModel):
    format: str = Field(..., description="Trend format name, e.g. 'POV'")
    reason: str = Field(..., description="Why this trend fits the product")


class MemeInfo(BaseModel):
    format: str = Field(..., description="Meme format name")
    search_query: str = Field(..., description="Search query for Tenor GIF")


class DialogueLine(BaseModel):
    speaker: str = Field(..., description="Who is speaking")
    line: str = Field(..., description="Dialogue line")


class ScriptScene(BaseModel):
    time: str = Field(..., description="Timestamp range, e.g. '0-3 sec'")
    visual: str = Field(..., description="What the viewer sees")
    voice: str = Field(..., description="Voiceover or spoken text")
    text_overlay: str = Field(..., description="On-screen text overlay")


class AIResponse(BaseModel):
    """Exact schema Gemini must conform to."""
    viral_score: int = Field(..., ge=0, le=100, description="Predicted virality 0-100")
    trend: TrendInfo
    hook: str = Field(..., description="Attention-grabbing opening line")
    meme: MemeInfo
    dialogue: List[DialogueLine] = Field(default_factory=list)
    script: List[ScriptScene] = Field(default_factory=list)
    caption: str = Field(..., description="Social media post caption")
    hashtags: List[str] = Field(default_factory=list, description="Relevant hashtags")


# ── Tenor GIF result ──────────────────────────────────────────────────────────

class GifResult(BaseModel):
    id: str
    title: str
    preview_url: str
    gif_url: str
    width: Optional[int] = None
    height: Optional[int] = None


# ── Meme section in the full response (adds optional GIF) ────────────────────

class MemeWithGif(BaseModel):
    format: str
    search_query: str
    gif: Optional[GifResult] = None


# ── Generation request ────────────────────────────────────────────────────────

class GenerateRequest(BaseModel):
    product_id: int = Field(..., description="ID of the product to generate content for")

    model_config = {"json_schema_extra": {"example": {"product_id": 1}}}


# ── Full content generation response ─────────────────────────────────────────

class ContentResponse(BaseModel):
    generation_id: int
    viral_score: int
    trend: TrendInfo
    hook: str
    meme: MemeWithGif
    dialogue: List[DialogueLine]
    script: List[ScriptScene]
    caption: str
    hashtags: List[str]
