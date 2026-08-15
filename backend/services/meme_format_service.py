from sqlite3 import Row
from typing import Any


GENERIC_MEME_FORMATS = {
    "",
    "meme",
    "pov",
    "pov meme",
    "reaction meme",
    "viral meme",
    "funny meme",
    "expectation vs reality",
}


FORMAT_RULES = [
    (("exam", "study", "assignment", "deadline", "panic"), "Exam Panic POV"),
    (("luxury", "premium", "elegant", "exclusive", "high-end"), "Luxury Reveal"),
    (("before", "after", "transform", "glow", "upgrade", "change"), "Before/After Glow-Up"),
    (("friend", "bro", "group", "squad", "chat"), "That One Friend"),
    (("work", "office", "founder", "startup", "professional"), "Work Mode vs Life Mode"),
    (("food", "drink", "snack", "taste", "craving"), "Craving Trigger"),
    (("fitness", "gym", "health", "routine"), "Day One vs Day Thirty"),
    (("money", "price", "budget", "cheap", "expensive"), "Budget Brain vs Main Character"),
    (("problem", "stress", "panic", "annoying", "struggle"), "POV Problem Solved"),
    (("reaction", "funny", "sarcastic", "roast"), "Instant Reaction Meme"),
    (("student", "college", "campus", "hostel"), "Campus Relatable POV"),
]


def choose_meme_format(product: Row, content: dict[str, Any], tone: str, requirements: str | None = None) -> str:
    current = str(content.get("meme_format") or "").strip()
    content_text = " ".join(
        [
            str(tone),
            str(requirements or ""),
            str(content.get("hook", "")),
            str(content.get("caption", "")),
            str(content.get("klipy_query", "")),
        ]
    ).lower()
    product_text = " ".join(
        [
            str(product["name"]),
            str(product["category"]),
            str(product["description"]),
            str(product["audience"]),
        ]
    ).lower()

    if current.lower() not in GENERIC_MEME_FORMATS:
        return current

    for text in (content_text, product_text):
        for keywords, meme_format in FORMAT_RULES:
            if any(keyword in text for keyword in keywords):
                return meme_format

    return f"{product['audience']} Relatable POV"
