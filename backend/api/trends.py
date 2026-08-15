from fastapi import APIRouter

from schemas.trends import TrendAnalyzeRequest, TrendAnalyzeResponse
from services.trend_intelligence_service import analyze_brand_trends


router = APIRouter(prefix="/api/trends", tags=["trends"])


@router.post("/analyze", response_model=TrendAnalyzeResponse)
async def analyze_trends(payload: TrendAnalyzeRequest):
    return await analyze_brand_trends(payload)
