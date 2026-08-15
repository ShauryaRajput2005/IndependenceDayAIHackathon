"""
tests/test_content.py — Tests for product creation and content generation endpoints.
Database setup is handled by conftest.py.
External services (Gemini, Tenor) are mocked.
"""
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app, raise_server_exceptions=False)

# ── Test data ──────────────────────────────────────────────────────────────────

SAMPLE_PRODUCT = {
    "name": "AI Resume Builder",
    "category": "Education",
    "description": "Creates ATS-friendly resumes with AI",
    "features": ["ATS optimization", "AI suggestions"],
    "problem_solved": "Students can't get callbacks",
    "target_audience": "Indian college students",
    "price": "Free",
    "platform": "instagram",
    "tone": "sarcastic",
    "requirements": "Make it Hinglish and meme-heavy",
}

MOCK_AI_RESPONSE = {
    "viral_score": 87,
    "trend": {"format": "POV", "reason": "Strong fit for college students"},
    "hook": "POV: Your resume gets rejected before HR even opens it",
    "meme": {"format": "POV", "search_query": "student panic"},
    "dialogue": [
        {"speaker": "Friend", "line": "Bhai resume bheja?"},
        {"speaker": "Me", "line": "Haan. HR ne bhi nahi dekha."},
    ],
    "script": [
        {
            "time": "0-3 sec",
            "visual": "Student staring at rejection email",
            "voice": "POV: Your resume gets rejected before HR even opens it",
            "text_overlay": "Rejected again",
        }
    ],
    "caption": "Bro's resume needs therapy",
    "hashtags": ["#studentlife", "#resume", "#jobs"],
}


# ── Tests ──────────────────────────────────────────────────────────────────────

def test_health_endpoint():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["service"] == "trendpilot-backend"


def test_create_product_success():
    resp = client.post("/api/product/create", json=SAMPLE_PRODUCT)
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["id"] > 0
    assert data["message"] == "Product created successfully"


def test_get_product_success():
    create_resp = client.post("/api/product/create", json=SAMPLE_PRODUCT)
    assert create_resp.status_code == 201, create_resp.text
    product_id = create_resp.json()["id"]

    resp = client.get(f"/api/product/{product_id}")
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["id"] == product_id
    assert data["name"] == SAMPLE_PRODUCT["name"]
    assert data["tone"] == SAMPLE_PRODUCT["tone"]
    assert isinstance(data["features"], list)


def test_get_product_not_found():
    resp = client.get("/api/product/9999")
    assert resp.status_code == 404


def test_generate_content_product_not_found():
    resp = client.post("/api/content/generate", json={"product_id": 9999})
    assert resp.status_code == 404


def test_generate_content_success():
    from schemas.content import AIResponse

    create_resp = client.post("/api/product/create", json=SAMPLE_PRODUCT)
    assert create_resp.status_code == 201, create_resp.text
    product_id = create_resp.json()["id"]

    mock_ai = AIResponse(**MOCK_AI_RESPONSE)

    with patch(
        "services.llm_service.LLMService.generate_content",
        new_callable=AsyncMock,
        return_value=mock_ai,
    ), patch(
        "services.tenor_service.search_gif",
        new_callable=AsyncMock,
        return_value=None,
    ):
        resp = client.post("/api/content/generate", json={"product_id": product_id})

    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "generation_id" in data
    assert data["viral_score"] == 87
    assert data["hook"] == MOCK_AI_RESPONSE["hook"]
    assert data["trend"]["format"] == "POV"
    assert len(data["dialogue"]) == 2
    assert len(data["script"]) == 1
    assert data["caption"] == MOCK_AI_RESPONSE["caption"]
    assert len(data["hashtags"]) == 3
    assert data["meme"]["gif"] is None


def test_generate_content_response_has_all_required_fields():
    from schemas.content import AIResponse

    create_resp = client.post("/api/product/create", json=SAMPLE_PRODUCT)
    assert create_resp.status_code == 201, create_resp.text
    product_id = create_resp.json()["id"]

    mock_ai = AIResponse(**MOCK_AI_RESPONSE)

    with patch(
        "services.llm_service.LLMService.generate_content",
        new_callable=AsyncMock,
        return_value=mock_ai,
    ), patch(
        "services.tenor_service.search_gif",
        new_callable=AsyncMock,
        return_value=None,
    ):
        resp = client.post("/api/content/generate", json={"product_id": product_id})

    assert resp.status_code == 200, resp.text
    data = resp.json()
    required_fields = [
        "generation_id", "viral_score", "trend", "hook",
        "meme", "dialogue", "script", "caption", "hashtags",
    ]
    for field in required_fields:
        assert field in data, f"Missing field: {field}"
