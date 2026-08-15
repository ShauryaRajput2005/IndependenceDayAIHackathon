"""
config.py — Centralised settings loaded from .env
"""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gemini_api_key: str = ""
    klipy_api_key: str = ""
    # tenor_api_key kept as alias for backwards compatibility
    tenor_api_key: str = ""
    tenor_client_key: str = "trendpilot"
    database_url: str = "sqlite:///./trendpilot.db"
    frontend_url: str = "http://localhost:5173"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()
