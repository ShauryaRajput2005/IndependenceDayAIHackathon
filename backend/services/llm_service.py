"""
services/llm_service.py — Gemini 2.5 Flash integration with structured output.
Only this module knows about the Gemini SDK.
"""
import asyncio
import time
from typing import Optional

from config import get_settings
from schemas.content import AIResponse
from utils.logger import get_logger
from utils.json_parser import extract_json_block, parse_and_validate

logger = get_logger(__name__)


class LLMService:
    """
    Abstraction over the Gemini API.
    Replace this class to swap providers without touching the rest of the app.
    """

    MODEL = "gemini-2.5-flash"

    def __init__(self):
        self._client = None

    def _get_client(self):
        """Lazy-initialise the Gemini client."""
        if self._client is None:
            from google import genai  # local import keeps startup fast if key missing

            settings = get_settings()
            if not settings.gemini_api_key:
                raise RuntimeError(
                    "GEMINI_API_KEY is not configured. "
                    "Add it to backend/.env before generating content."
                )
            self._client = genai.Client(api_key=settings.gemini_api_key)
        return self._client

    async def generate_content(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> AIResponse:
        """
        Call Gemini with structured output and return a validated AIResponse.
        Raises:
            ValueError   — schema validation failed
            RuntimeError — API key missing
            Exception    — provider-level errors (rate limit, unavailable, etc.)
        """
        from google.genai import types  # local import

        client = self._get_client()
        start = time.perf_counter()

        logger.info("Calling Gemini %s for structured content generation…", self.MODEL)

        try:
            # Run the synchronous Gemini call in a thread to avoid blocking the event loop
            response = await asyncio.to_thread(
                client.models.generate_content,
                model=self.MODEL,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    response_mime_type="application/json",
                    response_schema=AIResponse,
                ),
            )
        except Exception as exc:
            elapsed = time.perf_counter() - start
            logger.error("Gemini call failed after %.2fs: %s", elapsed, exc)
            self._map_provider_error(exc)

        elapsed = time.perf_counter() - start
        logger.info("Gemini responded in %.2fs", elapsed)

        # Extract and validate the structured response
        raw = response.text or ""
        cleaned = extract_json_block(raw)
        result = parse_and_validate(cleaned, AIResponse)

        return result

    @staticmethod
    def _map_provider_error(exc: Exception) -> None:
        """Re-raise provider errors with cleaner messages."""
        msg = str(exc).lower()
        if "quota" in msg or "rate" in msg or "429" in msg:
            raise Exception(f"RATE_LIMIT: Gemini rate limit reached. Try again shortly.") from exc
        if "api_key" in msg or "invalid" in msg or "403" in msg or "401" in msg:
            raise RuntimeError("INVALID_KEY: Gemini API key is invalid or unauthorised.") from exc
        if "unavailable" in msg or "503" in msg:
            raise Exception("UNAVAILABLE: Gemini service is temporarily unavailable.") from exc
        raise Exception(f"LLM_ERROR: {exc}") from exc


# Module-level singleton
llm_service = LLMService()
