"""
tests/test_tenor.py — Tests for Klipy GIF service: disabled mode, failure fallback, normalisation.
No real HTTP calls are made.
"""
import pytest
import httpx
from unittest.mock import AsyncMock, patch, MagicMock


# ── Klipy disabled (no API key) ───────────────────────────────────────────────

@pytest.mark.asyncio
async def test_klipy_disabled_when_no_api_key():
    """search_gif returns None when neither KLIPY_API_KEY nor TENOR_API_KEY is set."""
    from services.tenor_service import search_gif

    with patch("services.tenor_service.get_settings") as mock_settings:
        mock_settings.return_value.klipy_api_key = ""
        mock_settings.return_value.tenor_api_key = ""
        result = await search_gif("student panic")

    assert result is None


# ── Klipy HTTP failure ────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_klipy_returns_none_on_http_error():
    """search_gif returns None when Klipy returns an HTTP error."""
    from services.tenor_service import search_gif

    with patch("services.tenor_service.get_settings") as mock_settings, \
         patch("httpx.AsyncClient") as mock_client_cls:

        mock_settings.return_value.klipy_api_key = "fake_key"
        mock_settings.return_value.tenor_api_key = ""

        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "403 Forbidden", request=MagicMock(), response=MagicMock(status_code=403)
        )

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value=mock_resp)
        mock_client_cls.return_value = mock_client

        result = await search_gif("test query")

    assert result is None


@pytest.mark.asyncio
async def test_klipy_returns_none_on_request_error():
    """search_gif returns None on network/connection errors."""
    from services.tenor_service import search_gif

    with patch("services.tenor_service.get_settings") as mock_settings, \
         patch("httpx.AsyncClient") as mock_client_cls:

        mock_settings.return_value.klipy_api_key = "fake_key"
        mock_settings.return_value.tenor_api_key = ""

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(side_effect=httpx.RequestError("Connection refused"))
        mock_client_cls.return_value = mock_client

        result = await search_gif("test query")

    assert result is None


# ── Result normalisation ──────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_klipy_result_normalisation():
    """search_gif correctly normalises a valid Klipy response."""
    from services.tenor_service import search_gif

    mock_klipy_response = {
        "results": [
            {
                "id": "abc123",
                "title": "Student Panic GIF",
                "content_description": "Student panic meme",
                "media_formats": {
                    "tinygif": {
                        "url": "https://klipy.com/preview.gif",
                        "dims": [220, 160],
                    },
                    "gif": {
                        "url": "https://klipy.com/full.gif",
                        "dims": [498, 372],
                    },
                },
            }
        ]
    }

    with patch("services.tenor_service.get_settings") as mock_settings, \
         patch("httpx.AsyncClient") as mock_client_cls:

        mock_settings.return_value.klipy_api_key = "fake_key"
        mock_settings.return_value.tenor_api_key = ""

        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json = MagicMock(return_value=mock_klipy_response)

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value=mock_resp)
        mock_client_cls.return_value = mock_client

        result = await search_gif("student panic")

    assert result is not None
    assert result.id == "abc123"
    assert result.title == "Student Panic GIF"
    assert result.preview_url == "https://klipy.com/preview.gif"
    assert result.gif_url == "https://klipy.com/full.gif"
    assert result.width == 498
    assert result.height == 372


@pytest.mark.asyncio
async def test_klipy_empty_results():
    """search_gif returns None when Klipy returns no results."""
    from services.tenor_service import search_gif

    with patch("services.tenor_service.get_settings") as mock_settings, \
         patch("httpx.AsyncClient") as mock_client_cls:

        mock_settings.return_value.klipy_api_key = "fake_key"
        mock_settings.return_value.tenor_api_key = ""

        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json = MagicMock(return_value={"results": []})

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value=mock_resp)
        mock_client_cls.return_value = mock_client

        result = await search_gif("obscure meme query")

    assert result is None


@pytest.mark.asyncio
async def test_klipy_fallback_uses_tenor_key():
    """If KLIPY_API_KEY is empty, falls back to TENOR_API_KEY."""
    from services.tenor_service import search_gif

    with patch("services.tenor_service.get_settings") as mock_settings, \
         patch("httpx.AsyncClient") as mock_client_cls:

        mock_settings.return_value.klipy_api_key = ""
        mock_settings.return_value.tenor_api_key = "legacy_tenor_key"

        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json = MagicMock(return_value={"results": []})

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value=mock_resp)
        mock_client_cls.return_value = mock_client

        # Should attempt a request (not return None early) even with legacy key
        result = await search_gif("test")

    # The request was made (no None from key-missing guard)
    mock_client.get.assert_called_once()
