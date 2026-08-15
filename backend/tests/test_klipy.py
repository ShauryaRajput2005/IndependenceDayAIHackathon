import asyncio
import os
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.klipy_service import fetch_klipy_meme, get_trending_media, search_klipy_media


class KlipyServiceTest(unittest.TestCase):
    def setUp(self):
        self.previous_key = os.environ.pop("KLIPY_API_KEY", None)

    def tearDown(self):
        if self.previous_key is not None:
            os.environ["KLIPY_API_KEY"] = self.previous_key

    def test_fetch_klipy_meme_without_key_returns_fallback(self):
        result = asyncio.run(fetch_klipy_meme("student panic"))

        self.assertTrue(result["title"])
        self.assertIsNone(result["url"])
        self.assertIsNone(result["preview"])
        self.assertEqual(result["source"], "fallback")

    def test_search_klipy_media_without_key_returns_normalized_fallback(self):
        result = asyncio.run(search_klipy_media("school lunch nostalgia", media_type="meme", limit=2))

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["mediaType"], "meme")
        self.assertEqual(result[0]["source"], "klipy_fallback")
        self.assertEqual(result[0]["providerStatus"], "missing_klipy_api_key")
        self.assertTrue(result[0]["tags"])

    def test_get_trending_media_without_key_supports_media_types(self):
        result = asyncio.run(get_trending_media(media_type="clip", limit=2))

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["mediaType"], "clip")
        self.assertEqual(result[0]["providerStatus"], "missing_klipy_api_key")
        self.assertGreater(result[0]["views"], 0)


if __name__ == "__main__":
    unittest.main()
