"""
utils/json_parser.py — Safe JSON parsing with controlled error handling.
Used as a defensive layer even when Gemini structured output is active.
"""
import json
from typing import Any, Optional, Type, TypeVar

from pydantic import BaseModel, ValidationError

from utils.logger import get_logger

logger = get_logger(__name__)

T = TypeVar("T", bound=BaseModel)


def safe_parse_json(raw: str) -> Optional[dict]:
    """
    Parse a raw string as JSON.
    Returns None on failure instead of raising.
    """
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError) as exc:
        logger.error("JSON parse error: %s | raw snippet: %.200s", exc, raw)
        return None


def parse_and_validate(raw: str, model: Type[T]) -> T:
    """
    Parse raw JSON and validate it against a Pydantic model.
    Raises ValueError with a clear message on failure.
    """
    data = safe_parse_json(raw)
    if data is None:
        raise ValueError(f"Response is not valid JSON. Snippet: {raw[:200]}")
    try:
        return model.model_validate(data)
    except ValidationError as exc:
        logger.error("Schema validation failed for %s: %s", model.__name__, exc)
        raise ValueError(f"AI response did not match expected schema: {exc}") from exc


def extract_json_block(text: str) -> str:
    """
    Strip markdown code fences (```json ... ```) if present.
    Gemini sometimes wraps output in fences even with structured output.
    """
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        # Drop first and last fence lines
        inner = lines[1:] if lines[0].startswith("```") else lines
        if inner and inner[-1].strip() == "```":
            inner = inner[:-1]
        text = "\n".join(inner)
    return text
