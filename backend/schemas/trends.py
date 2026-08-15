from typing import Literal

from pydantic import BaseModel, Field


MediaType = Literal["gif", "meme", "sticker", "clip", "emoji"]


class TrendAnalyzeRequest(BaseModel):
    brand: str = Field(..., min_length=1, max_length=120)
    industry: str = Field(..., min_length=1, max_length=120)
    audience: str = Field(default="Gen Z", max_length=120)
    limit: int = Field(default=10, ge=1, le=25)


class TrendItem(BaseModel):
    id: str
    title: str
    mediaType: MediaType
    source: str
    views: int | None = None
    shares: int | None = None
    likes: int | None = None
    tags: list[str] = []
    url: str | None = None
    preview: str | None = None
    freshness: float = Field(default=70, ge=0, le=100)
    providerStatus: str | None = None


class TrendSource(BaseModel):
    source: str
    trends: list[TrendItem]


class TrendAnalysis(BaseModel):
    trendId: str
    trendScore: int = Field(..., ge=0, le=100)
    trendCategory: str
    audience: str
    recommendedMediaType: MediaType
    reason: str
    viralPotential: float = Field(..., ge=0, le=100)
    relevance: float = Field(..., ge=0, le=100)
    engagement: float = Field(..., ge=0, le=100)
    freshness: float = Field(..., ge=0, le=100)


class RankedTrend(TrendItem):
    score: float = Field(..., ge=0, le=100)
    analysis: TrendAnalysis


class MediaSuggestions(BaseModel):
    recommendedMemes: list[TrendItem] = []
    recommendedGifs: list[TrendItem] = []
    recommendedClips: list[TrendItem] = []
    recommendedStickers: list[TrendItem] = []
    recommendedEmojis: list[TrendItem] = []


class TrendPrediction(BaseModel):
    futureTrend: str
    confidence: float = Field(..., ge=0, le=1)
    growthPrediction: str
    basis: str


class ContentSuggestions(BaseModel):
    captions: list[str]
    reelIdeas: list[str]
    hashtags: list[str]
    cta: list[str]


class TrendAnalyzeResponse(BaseModel):
    topTrends: list[RankedTrend]
    predictions: list[TrendPrediction]
    mediaSuggestions: MediaSuggestions
    captions: list[str]
    reelIdeas: list[str]
    hashtags: list[str]
    cta: list[str]
    sources: list[TrendSource]
    latencyMs: int
