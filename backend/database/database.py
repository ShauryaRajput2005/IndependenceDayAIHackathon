"""
database/database.py — SQLite engine, session factory, and table initialisation.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config import get_settings
from utils.logger import get_logger

logger = get_logger(__name__)

settings = get_settings()

# connect_args only needed for SQLite (thread safety)
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def init_db() -> None:
    """Create all tables if they do not already exist."""
    # Import models here so Base sees them before create_all
    import database.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    logger.info("Database initialised — tables ready.")


def get_db():
    """FastAPI dependency that yields a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
