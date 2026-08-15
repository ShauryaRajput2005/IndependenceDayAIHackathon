import json

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from database.database import execute, fetch_one
from schemas.content import ContentGenerateRequest, ContentGenerateResponse, GeneratedContent
from services.llm_service import generate_content
from services.klipy_service import fetch_klipy_meme
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
    meme = await fetch_klipy_meme(str(raw_content.get("klipy_query", product["name"])))
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
