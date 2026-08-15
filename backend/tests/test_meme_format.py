import unittest
from collections import UserDict

from services.meme_format_service import choose_meme_format


class ProductRow(UserDict):
    def __getitem__(self, key):
        return self.data[key]


class MemeFormatServiceTest(unittest.TestCase):
    def test_selects_exam_specific_format(self):
        product = ProductRow(
            {
                "name": "CampusWear",
                "category": "Consumer Brand",
                "description": "Oversized t-shirt for college students",
                "audience": "College students",
            }
        )
        content = {
            "meme_format": "POV Meme",
            "hook": "POV: exam week panic but your outfit is sorted",
            "caption": "Campus chaos, clean fit.",
            "klipy_query": "student exam panic oversized t-shirt",
        }

        self.assertEqual(choose_meme_format(product, content, "Meme Style"), "Exam Panic POV")

    def test_keeps_specific_ai_format_when_no_rule_matches(self):
        product = ProductRow(
            {
                "name": "Nimbus",
                "category": "Tools",
                "description": "A focused planning app",
                "audience": "Designers",
            }
        )
        content = {"meme_format": "Calendar Villain Arc", "hook": "Your deadlines got a plot twist"}

        self.assertEqual(choose_meme_format(product, content, "Funny"), "Calendar Villain Arc")


if __name__ == "__main__":
    unittest.main()
