"""
api/content.py — Content generation endpoint.

Pipeline:
  Load Product → Load Preferences → Load Trends → Build Prompt
  → Gemini Structured Output → Tenor Search → Save → Return
"""
import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Product, Generation
from schemas.content import GenerateRequest, ContentResponse, MemeWithGif
from services.llm_service import llm_service
from services import prompt_service
from services import trend_service
from services import memory_service
from services import klipy_service
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/content", tags=["Content"])


@router.post(
    "/generate",
    response_model=ContentResponse,
    summary="Generate viral content for a product",
)
async def generate_content(payload: GenerateRequest, db: Session = Depends(get_db)):
    """
    Run the complete content generation pipeline:
    1. Load product
    2. Load preference memory
    3. Load relevant trends and meme formats
    4. Build prompt
    5. Call Gemini with structured output
    6. Search Tenor for GIF (optional)
    7. Persist generation
    8. Return structured response
    """
    # ── 1. Load product ────────────────────────────────────────────────────────
    product: Product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {payload.product_id} not found")

    # ── 2. Load preference memory ──────────────────────────────────────────────
    memory_ctx = memory_service.build_memory_context(db, product.id)

    # ── 3. Load trend context ──────────────────────────────────────────────────
    trends = trend_service.get_relevant_trends(
        platform=product.platform,
        tone=product.tone,
        audience=product.target_audience or "",
    )
    meme_formats = trend_service.get_relevant_meme_formats(
        tone=product.tone,
        audience=product.target_audience or "",
    )

    # ── 4. Build prompts ───────────────────────────────────────────────────────
    system_prompt = prompt_service.build_system_prompt()
    user_prompt = prompt_service.build_content_prompt(
        product=product,
        memory_context=memory_ctx,
        trends=trends,
        meme_formats=meme_formats,
    )

    # ── 5. Call Gemini ─────────────────────────────────────────────────────────
    try:
        ai_response = await llm_service.generate_content(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )
    except RuntimeError as exc:
        # Missing API key or auth error
        logger.error("LLM runtime error: %s", exc)
        raise HTTPException(status_code=503, detail="AI service configuration error. Check GEMINI_API_KEY.")
    except ValueError as exc:
        logger.error("AI response schema mismatch: %s", exc)
        raise HTTPException(status_code=500, detail="AI returned an unexpected response format.")
    except Exception as exc:
        msg = str(exc)
        logger.error("LLM generation error: %s", msg)
        if "RATE_LIMIT" in msg:
            raise HTTPException(status_code=429, detail="AI provider rate limit reached. Try again later.")
        if "UNAVAILABLE" in msg:
            raise HTTPException(status_code=503, detail="AI provider is temporarily unavailable.")
        raise HTTPException(status_code=500, detail="Content generation failed.")

    # ── 6. Tenor GIF search (optional) ────────────────────────────────────────
    gif = await klipy_service.search_gif(ai_response.meme.search_query)

    # ── 7. Persist generation ──────────────────────────────────────────────────
    response_payload = ai_response.model_dump()
    generation = Generation(
        product_id=product.id,
        response=json.dumps(response_payload),
    )
    db.add(generation)
    db.commit()
    db.refresh(generation)

    logger.info(
        "Generation saved: id=%d product_id=%d viral_score=%d",
        generation.id,
        product.id,
        ai_response.viral_score,
    )

    # ── 8. Build response ──────────────────────────────────────────────────────
    return ContentResponse(
        generation_id=generation.id,
        viral_score=ai_response.viral_score,
        trend=ai_response.trend,
        hook=ai_response.hook,
        meme=MemeWithGif(
            format=ai_response.meme.format,
            search_query=ai_response.meme.search_query,
            gif=gif,
        ),
        dialogue=ai_response.dialogue,
        script=ai_response.script,
        caption=ai_response.caption,
        hashtags=ai_response.hashtags,
    )
