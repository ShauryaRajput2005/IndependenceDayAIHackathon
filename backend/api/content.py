import json

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from database.database import execute, fetch_one
from schemas.content import ContentGenerateRequest, ContentGenerateResponse, GeneratedContent
from services.llm_service import generate_content
from services.klipy_service import fetch_klipy_media
from services.media_selector_service import choose_media_type_with_groq
from services.meme_format_service import choose_meme_format
from services.prompt_service import build_content_prompt
from services.trend_service import get_trends


router = APIRouter(prefix="/api/content", tags=["content"])


@router.post("/generate", response_model=ContentGenerateResponse)
async def create_content(payload: ContentGenerateRequest):
    product = fetch_one("SELECT * FROM products WHERE id = ?", (payload.product_id,))
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    tone = payload.tone or product["tone"]
    prompt = build_content_prompt(product, tone=tone, requirements=payload.requirements)
    raw_content = await generate_content(product, prompt, tone)

    raw_content.setdefault("trend", (get_trends() or [None])[0])
    raw_content["meme_format"] = choose_meme_format(product, raw_content, tone, payload.requirements)
    media_choice = await choose_media_type_with_groq(raw_content, tone)
    raw_content["selected_media_type"] = media_choice["media_type"]
    raw_content["media_feeling"] = media_choice["feeling"]
    raw_content["media_reason"] = media_choice["reason"]
    meme = await fetch_klipy_media(
        str(raw_content.get("klipy_query", product["name"])),
        media_type=media_choice["media_type"],
    )
    raw_content["meme"] = meme

    try:
        content = GeneratedContent.model_validate(raw_content)
    except ValidationError as exc:
        raise HTTPException(status_code=502, detail=f"AI response did not match content schema: {exc}") from exc

    generation_id = execute(
        """
        INSERT INTO generations (product_id, tone, response)
        VALUES (?, ?, ?)
        """,
        (payload.product_id, tone, content.model_dump_json()),
    )

    return {
        "generation_id": generation_id,
        "product_id": payload.product_id,
        **json.loads(content.model_dump_json()),
    }
