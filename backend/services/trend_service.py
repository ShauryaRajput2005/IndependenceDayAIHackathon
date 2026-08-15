import json
from pathlib import Path
from typing import Any


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def _load_json_file(name: str, fallback: list[dict[str, Any]]) -> list[dict[str, Any]]:
    path = DATA_DIR / name
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return fallback
    return data if isinstance(data, list) else fallback


def get_trends() -> list[dict[str, Any]]:
    return _load_json_file(
        "trends.json",
        [
            {"name": "POV", "use": "Relatable situations", "audience": "Gen-Z"},
            {"name": "Expectation vs Reality", "use": "Product contrast"},
            {"name": "Nobody meme", "use": "Unexpected humor"},
            {"name": "Starter pack", "use": "Audience identity jokes"},
        ],
    )


def get_meme_formats() -> list[dict[str, Any]]:
    return _load_json_file(
        "meme_formats.json",
        [
            {"name": "POV Meme", "best_for": "Personal struggle"},
            {"name": "Expectation vs Reality", "best_for": "Before and after"},
            {"name": "Two Buttons", "best_for": "Decision tension"},
        ],
    )
