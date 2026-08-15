"""
services/llm_service.py — OpenRouter integration with structured output.
"""
import asyncio
import time
import json
import openai

from config import get_settings
from schemas.content import AIResponse
from utils.logger import get_logger
from utils.json_parser import extract_json_block, parse_and_validate

logger = get_logger(__name__)


class LLMService:
    """
    Abstraction over the LLM API using OpenRouter via OpenAI client.
    """

    MODEL = "google/gemini-2.5-flash"

    def __init__(self):
        self._client = None

    def _get_client(self):
        """Lazy-initialise the OpenAI client pointing to OpenRouter."""
        if self._client is None:

            settings = get_settings()
            # Fallback to gemini_api_key if openrouter_api_key isn't set, just in case user mixed them up
            api_key = settings.openrouter_api_key or settings.gemini_api_key
            if not api_key:
                raise RuntimeError(
                    "OPENROUTER_API_KEY is not configured. "
                    "Add it to backend/.env before generating content."
                )
            self._client = openai.AsyncOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
            )
        return self._client

    async def generate_content(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> AIResponse:
        """
        Call OpenRouter and return a validated AIResponse.
        Raises:
            ValueError   — schema validation failed
            RuntimeError — API key missing
            Exception    — provider-level errors
        """
        client = self._get_client()
        start = time.perf_counter()

        logger.info("Calling OpenRouter (%s) for structured content generation…", self.MODEL)

        try:
            response = await client.chat.completions.create(
                model=self.MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                extra_headers={
                    "HTTP-Referer": "http://localhost:5173", # Optional, for OpenRouter rankings
                    "X-Title": "TrendPilot AI", # Optional, for OpenRouter rankings
                }
            )
        except Exception as exc:
            elapsed = time.perf_counter() - start
            logger.error("OpenRouter call failed after %.2fs: %s", elapsed, exc)
            self._map_provider_error(exc)

        elapsed = time.perf_counter() - start
        logger.info("OpenRouter responded in %.2fs", elapsed)

        # Extract and validate the structured response
        raw = response.choices[0].message.content or ""
        cleaned = extract_json_block(raw)
        result = parse_and_validate(cleaned, AIResponse)

        return result

    @staticmethod
    def _map_provider_error(exc: Exception) -> None:
        """Re-raise provider errors with cleaner messages."""
        msg = str(exc).lower()
        if "quota" in msg or "rate" in msg or "429" in msg:
            raise Exception(f"RATE_LIMIT: OpenRouter rate limit reached. Try again shortly.") from exc
        if "api_key" in msg or "invalid" in msg or "403" in msg or "401" in msg:
            raise RuntimeError("INVALID_KEY: OpenRouter API key is invalid or unauthorised.") from exc
        if "unavailable" in msg or "503" in msg:
            raise Exception("UNAVAILABLE: OpenRouter service is temporarily unavailable.") from exc
        raise Exception(f"LLM_ERROR: {exc}") from exc


# Module-level singleton
llm_service = LLMService()
