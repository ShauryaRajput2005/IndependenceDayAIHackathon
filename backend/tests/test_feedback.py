"""
tests/test_feedback.py — Tests for feedback submission and preference storage.
Database setup is handled by conftest.py.
"""
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app, raise_server_exceptions=False)

SAMPLE_PRODUCT = {
    "name": "AI Resume Builder",
    "category": "Education",
    "description": "Creates ATS-friendly resumes",
    "features": ["ATS optimization"],
    "platform": "instagram",
    "tone": "sarcastic",
}

MOCK_AI_RESPONSE = {
    "viral_score": 80,
    "trend": {"format": "POV", "reason": "Good fit"},
    "hook": "Test hook",
    "meme": {"format": "POV", "search_query": "test"},
    "dialogue": [],
    "script": [],
    "caption": "Test caption",
    "hashtags": ["#test"],
}


def _create_product_and_generation():
    from schemas.content import AIResponse

    prod_resp = client.post("/api/product/create", json=SAMPLE_PRODUCT)
    assert prod_resp.status_code == 201, prod_resp.text
    product_id = prod_resp.json()["id"]

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
        gen_resp = client.post("/api/content/generate", json={"product_id": product_id})

    assert gen_resp.status_code == 200, gen_resp.text
    return gen_resp.json()["generation_id"], product_id


def test_feedback_creation_success():
    gen_id, _ = _create_product_and_generation()
    resp = client.post("/api/feedback", json={
        "generation_id": gen_id,
        "feedback_type": "funnier",
        "comment": "Add more savage humour",
    })
    assert resp.status_code == 201, resp.text
    data = resp.json()
    assert data["generation_id"] == gen_id
    assert data["feedback_type"] == "funnier"
    assert data["preference_saved"] is True


def test_feedback_like_creates_positive_preference():
    gen_id, _ = _create_product_and_generation()
    resp = client.post("/api/feedback", json={"generation_id": gen_id, "feedback_type": "like"})
    assert resp.status_code == 201, resp.text
    assert resp.json()["preference_saved"] is True


def test_feedback_dislike_creates_negative_preference():
    gen_id, _ = _create_product_and_generation()
    resp = client.post("/api/feedback", json={"generation_id": gen_id, "feedback_type": "dislike"})
    assert resp.status_code == 201, resp.text
    assert resp.json()["preference_saved"] is True


def test_feedback_invalid_generation_id():
    resp = client.post("/api/feedback", json={"generation_id": 9999, "feedback_type": "funnier"})
    assert resp.status_code == 404


def test_preference_appears_in_next_generation_context():
    from schemas.content import AIResponse

    gen_id, product_id = _create_product_and_generation()
    client.post("/api/feedback", json={"generation_id": gen_id, "feedback_type": "funnier"})

    captured_prompts = []

    async def mock_generate(self, system_prompt, user_prompt):
        captured_prompts.append(user_prompt)
        return AIResponse(**MOCK_AI_RESPONSE)

    with patch("services.llm_service.LLMService.generate_content", new=mock_generate), \
         patch("services.tenor_service.search_gif", new_callable=AsyncMock, return_value=None):
        client.post("/api/content/generate", json={"product_id": product_id})

    assert captured_prompts, "No prompt was captured"
    assert "humor" in captured_prompts[0].lower() or "sarcastic" in captured_prompts[0].lower()


def test_all_feedback_types_accepted():
    feedback_types = [
        "funnier", "more_trendy", "more_relatable", "more_professional",
        "better_hook", "shorter", "like", "dislike",
    ]
    gen_id, _ = _create_product_and_generation()
    for fb_type in feedback_types:
        resp = client.post("/api/feedback", json={"generation_id": gen_id, "feedback_type": fb_type})
        assert resp.status_code == 201, f"Failed for feedback_type={fb_type}: {resp.text}"
