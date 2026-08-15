import time
from typing import Any
import json
import os


_CACHE: dict[str, tuple[float, Any]] = {}


def _redis_client():
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        return None
    try:
        import redis

        return redis.Redis.from_url(redis_url, decode_responses=True)
    except Exception:
        return None


def get_cache(key: str) -> Any | None:
    client = _redis_client()
    if client:
        try:
            raw = client.get(key)
            return json.loads(raw) if raw else None
        except Exception:
            pass

    item = _CACHE.get(key)
    if not item:
        return None
    expires_at, value = item
    if time.time() > expires_at:
        _CACHE.pop(key, None)
        return None
    return value


def set_cache(key: str, value: Any, ttl_seconds: int = 900) -> None:
    client = _redis_client()
    if client:
        try:
            client.setex(key, ttl_seconds, json.dumps(value))
            return
        except Exception:
            pass

    _CACHE[key] = (time.time() + ttl_seconds, value)
