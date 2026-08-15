"""
services/prompt_service.py — Builds system + content prompts from product + context.
"""
from typing import List

from database.models import Product
from prompts.system import SYSTEM_PROMPT
from prompts.content import CONTENT_PROMPT_TEMPLATE
from prompts.meme import format_meme_context
from services.trend_service import format_trends_for_prompt


def build_system_prompt() -> str:
    """Return the static system prompt."""
    return SYSTEM_PROMPT


def build_content_prompt(
    product: Product,
    memory_context: str,
    trends: List[dict],
    meme_formats: List[dict],
) -> str:
    """
    Assemble the full user-turn prompt from product data, memory, and trends.
    All fields are injected to prevent the LLM from missing context.
    """
    features_str = "\n".join(f"  • {f}" for f in product.features_list) or "  • No features listed"
    requirements = (product.requirements or "No specific requirements — use creative judgment.").strip()
    problem = (product.problem_solved or "Not specified").strip()
    audience = (product.target_audience or "General audience").strip()
    price = (product.price or "Not specified").strip()

    trends_text = format_trends_for_prompt(trends)
    meme_text = format_meme_context(meme_formats)

    prompt = CONTENT_PROMPT_TEMPLATE.format(
        product_name=product.name,
        category=product.category,
        description=product.description,
        features=features_str,
        problem=problem,
        audience=audience,
        price=price,
        platform=product.platform,
        tone=product.tone,
        requirements=requirements,
        preferences=memory_context,
        trends=trends_text,
        meme_formats=meme_text,
    )
    return prompt.strip()
