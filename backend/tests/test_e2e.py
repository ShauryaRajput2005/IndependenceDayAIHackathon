import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


class BackendE2ETest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = _free_port()
        cls.base_url = f"http://127.0.0.1:{cls.port}"
        cls.db_file = tempfile.NamedTemporaryFile(prefix="trendpilot-e2e-", suffix=".db", delete=False)
        cls.db_file.close()

        env = os.environ.copy()
        env.update(
            {
                "DATABASE_URL": f"sqlite:///{cls.db_file.name}",
                "GEMINI_API_KEY": "",
                "OPENROUTER_API_KEY": "",
                "GROQ_API_KEY": "",
                "KLIPY_API_KEY": "",
            }
        )

        cls.server = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "main:app",
                "--app-dir",
                "backend",
                "--host",
                "127.0.0.1",
                "--port",
                str(cls.port),
            ],
            cwd=ROOT_DIR,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        for _ in range(30):
            try:
                cls.get_json("/api/health")
                return
            except Exception:
                time.sleep(0.25)

        cls.tearDownClass()
        raise RuntimeError("Backend did not become ready for E2E tests.")

    @classmethod
    def tearDownClass(cls):
        server = getattr(cls, "server", None)
        if server and server.poll() is None:
            server.terminate()
            try:
                server.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server.kill()
        db_file = getattr(cls, "db_file", None)
        if db_file:
            Path(db_file.name).unlink(missing_ok=True)

    @classmethod
    def get_json(cls, path: str):
        with urllib.request.urlopen(f"{cls.base_url}{path}", timeout=5) as response:
            return json.loads(response.read().decode("utf-8"))

    @classmethod
    def post_json(cls, path: str, payload: dict):
        request = urllib.request.Request(
            f"{cls.base_url}{path}",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))

    @classmethod
    def status_for(cls, method: str, path: str, payload: dict | None = None) -> int:
        try:
            if method == "POST":
                cls.post_json(path, payload or {})
            else:
                cls.get_json(path)
            return 200
        except urllib.error.HTTPError as exc:
            status = int(exc.code)
            exc.close()
            return status

    def assert_required_keys(self, payload: dict, keys: set[str]):
        self.assertTrue(keys.issubset(payload.keys()), f"Missing keys: {keys - payload.keys()}")

    def test_all_backend_endpoints(self):
        root = self.get_json("/")
        health = self.get_json("/api/health")
        openapi = self.get_json("/openapi.json")

        product_payload = {
            "name": "AI Resume Builder",
            "category": "Education",
            "description": "AI platform for resume creation",
            "features": "ATS optimization, templates",
            "problem": "Students struggle to make ATS-friendly resumes",
            "audience": "College students",
            "price_range": "Free trial",
            "competitors": "Canva, Novoresume",
            "platform": "Instagram",
            "tone": "Funny",
            "requirements": "Make it relatable and meme style",
        }
        product = self.post_json(
            "/api/product/create",
            product_payload,
        )
        product_read = self.get_json(f"/api/product/{product['product_id']}")

        content_payload = {
            "product_id": product["product_id"],
            "tone": "Sarcastic",
            "requirements": "Use Hinglish and keep punchlines short",
        }
        content = self.post_json("/api/content/generate", content_payload)

        feedback_payload = {
            "generation_id": content["generation_id"],
            "feedback": "Make it funnier and less formal",
            "sentiment": "Positive",
        }
        feedback = self.post_json(
            "/api/feedback/create",
            feedback_payload,
        )
        brand = self.get_json(f"/api/brand/{product['product_id']}")
        recent = self.get_json("/api/recent?limit=5")
        trend_analysis = self.post_json(
            "/api/trends/analyze",
            {
                "brand": "Frooti",
                "industry": "Food & Beverage",
                "audience": "Gen Z",
                "limit": 10,
            },
        )

        self.assert_required_keys(root, {"name", "status"})
        self.assertEqual(root["status"], "ready")

        self.assert_required_keys(health, {"ok", "service"})
        self.assertTrue(health["ok"])

        self.assert_required_keys(product, {"product_id", "message"})
        self.assertGreater(product["product_id"], 0)
        self.assertEqual(product["message"], "Product saved successfully")

        self.assert_required_keys(product_read, {"id", "name", "category", "description", "audience", "platform", "tone"})
        self.assertEqual(product_read["id"], product["product_id"])
        for key, value in product_payload.items():
            self.assertEqual(product_read[key], value)

        self.assert_required_keys(
            content,
            {
                "generation_id",
                "product_id",
                "hook",
                "meme_format",
                "dialogue",
                "script",
                "caption",
                "klipy_query",
                "hashtags",
                "viral_score",
                "trend",
                "meme",
            },
        )
        self.assertEqual(content["product_id"], product["product_id"])
        self.assertGreater(content["generation_id"], 0)
        self.assertIsInstance(content["hook"], str)
        self.assertGreater(len(content["hook"]), 10)
        self.assertIsInstance(content["dialogue"], list)
        self.assertGreaterEqual(len(content["dialogue"]), 2)
        self.assertIsInstance(content["script"], list)
        self.assertGreaterEqual(len(content["script"]), 1)
        self.assert_required_keys(content["script"][0], {"scene", "time"})
        self.assertTrue(content["klipy_query"])
        self.assertGreaterEqual(content["viral_score"], 0)
        self.assertLessEqual(content["viral_score"], 100)
        self.assert_required_keys(content["meme"], {"title", "url", "preview", "source"})
        self.assertIn(content["meme"]["source"], {"fallback", "klipy", "klipy_empty", "klipy_unavailable"})

        self.assert_required_keys(feedback, {"feedback_id", "preference", "message"})
        self.assertGreater(feedback["feedback_id"], 0)
        self.assertEqual(feedback["preference"], feedback_payload["feedback"])

        self.assert_required_keys(brand, {"product", "memory", "recent_generations"})
        self.assertEqual(brand["product"]["id"], product["product_id"])
        self.assertIn("funnier", brand["memory"])
        self.assertGreaterEqual(len(brand["recent_generations"]), 1)
        self.assertEqual(brand["recent_generations"][0]["id"], content["generation_id"])

        self.assertEqual(len(recent), 1)
        self.assertEqual(recent[0]["generation_id"], content["generation_id"])
        self.assertEqual(recent[0]["product_id"], product["product_id"])
        self.assertEqual(recent[0]["product_name"], product_payload["name"])
        self.assertEqual(recent[0]["response"]["klipy_query"], content["klipy_query"])

        self.assert_required_keys(
            trend_analysis,
            {
                "topTrends",
                "predictions",
                "mediaSuggestions",
                "captions",
                "reelIdeas",
                "hashtags",
                "cta",
                "sources",
                "latencyMs",
            },
        )
        self.assertGreaterEqual(len(trend_analysis["topTrends"]), 1)
        self.assertLessEqual(len(trend_analysis["topTrends"]), 10)
        self.assertGreaterEqual(trend_analysis["topTrends"][0]["score"], trend_analysis["topTrends"][-1]["score"])
        self.assert_required_keys(
            trend_analysis["topTrends"][0],
            {"id", "title", "mediaType", "source", "tags", "score", "analysis"},
        )
        self.assert_required_keys(
            trend_analysis["topTrends"][0]["analysis"],
            {
                "trendScore",
                "trendCategory",
                "audience",
                "recommendedMediaType",
                "reason",
                "viralPotential",
                "relevance",
                "engagement",
                "freshness",
            },
        )
        self.assertGreaterEqual(len(trend_analysis["predictions"]), 1)
        self.assert_required_keys(
            trend_analysis["predictions"][0],
            {"futureTrend", "confidence", "growthPrediction", "basis"},
        )
        self.assert_required_keys(
            trend_analysis["mediaSuggestions"],
            {
                "recommendedMemes",
                "recommendedGifs",
                "recommendedClips",
                "recommendedStickers",
                "recommendedEmojis",
            },
        )
        self.assertGreaterEqual(len(trend_analysis["captions"]), 1)
        self.assertGreaterEqual(len(trend_analysis["reelIdeas"]), 1)
        self.assertGreaterEqual(len(trend_analysis["hashtags"]), 1)
        self.assertGreaterEqual(len(trend_analysis["cta"]), 1)
        self.assertGreaterEqual(len(trend_analysis["sources"]), 1)

        for path in {
            "/",
            "/api/health",
            "/api/product/create",
            "/api/product/{product_id}",
            "/api/content/generate",
            "/api/feedback/create",
            "/api/brand/{product_id}",
            "/api/recent",
            "/api/trends/analyze",
        }:
            self.assertIn(path, openapi["paths"])

        self.assertEqual(self.status_for("GET", "/api/product/999999"), 404)
        self.assertEqual(self.status_for("POST", "/api/content/generate", {"product_id": 999999}), 404)
        self.assertEqual(
            self.status_for("POST", "/api/feedback/create", {"generation_id": 999999, "feedback": "test"}),
            404,
        )
        self.assertEqual(self.status_for("POST", "/api/product/create", {"name": ""}), 422)
        self.assertEqual(self.status_for("POST", "/api/content/generate", {"product_id": 0}), 422)
        self.assertEqual(self.status_for("POST", "/api/trends/analyze", {"brand": ""}), 422)


if __name__ == "__main__":
    unittest.main()
