"""
tests/conftest.py — Shared pytest fixtures.
Sets up a per-module SQLite test database that's created before any test runs.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import database.models  # noqa: F401 — must import to register models with Base
from database.database import Base, get_db
from main import app

# Use file-based SQLite for tests (in-memory doesn't work reliably with
# TestClient because it runs in different threads)
TEST_DB_URL = "sqlite:///./test_trendpilot.db"

test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


# Apply override once at import time
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function", autouse=True)
def reset_db():
    """Drop and recreate all tables before every test function for isolation."""
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
