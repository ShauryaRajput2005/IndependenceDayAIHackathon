import os
import sqlite3
from pathlib import Path
from typing import Iterable

from database import models


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = BASE_DIR / "trendpilot.db"


def _database_path() -> Path:
    raw_url = os.getenv("DATABASE_URL", str(DEFAULT_DB_PATH))
    if raw_url.startswith("sqlite:///"):
        raw_url = raw_url.replace("sqlite:///", "", 1)
    return Path(raw_url)


def get_connection() -> sqlite3.Connection:
    db_path = _database_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript(
            "\n".join(
                [
                    models.CREATE_PRODUCTS_TABLE,
                    models.CREATE_PREFERENCES_TABLE,
                    models.CREATE_GENERATIONS_TABLE,
                    models.CREATE_FEEDBACK_TABLE,
                    models.CREATE_TREND_SNAPSHOTS_TABLE,
                    models.CREATE_TREND_ANALYSES_TABLE,
                    models.CREATE_TREND_PREDICTIONS_TABLE,
                ]
            )
        )


def fetch_one(query: str, params: Iterable = ()) -> sqlite3.Row | None:
    with get_connection() as conn:
        return conn.execute(query, tuple(params)).fetchone()


def fetch_all(query: str, params: Iterable = ()) -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(query, tuple(params)).fetchall()


def execute(query: str, params: Iterable = ()) -> int:
    with get_connection() as conn:
        cursor = conn.execute(query, tuple(params))
        conn.commit()
        return int(cursor.lastrowid)
