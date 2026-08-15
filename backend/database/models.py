"""
database/models.py — SQLAlchemy ORM models.
"""
import json
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    # features stored as JSON text: '["feat1", "feat2"]'
    features = Column(Text, nullable=False, default="[]")
    problem_solved = Column(Text, nullable=True)
    target_audience = Column(String(255), nullable=True)
    price = Column(String(100), nullable=True)
    platform = Column(String(50), nullable=False)
    tone = Column(String(50), nullable=False)
    requirements = Column(Text, nullable=True)
    created_at = Column(DateTime, default=_utcnow)

    generations = relationship("Generation", back_populates="product")
    preferences = relationship("Preference", back_populates="product")

    @property
    def features_list(self) -> list:
        try:
            return json.loads(self.features)
        except (json.JSONDecodeError, TypeError):
            return []

    @features_list.setter
    def features_list(self, value: list) -> None:
        self.features = json.dumps(value)


class Generation(Base):
    __tablename__ = "generations"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    # Full AI response stored as JSON text
    response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=_utcnow)

    product = relationship("Product", back_populates="generations")
    feedbacks = relationship("Feedback", back_populates="generation")

    @property
    def response_dict(self) -> dict:
        try:
            return json.loads(self.response)
        except (json.JSONDecodeError, TypeError):
            return {}


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    generation_id = Column(Integer, ForeignKey("generations.id"), nullable=False)
    feedback_type = Column(String(50), nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=_utcnow)

    generation = relationship("Generation", back_populates="feedbacks")


class Preference(Base):
    __tablename__ = "preferences"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    preference = Column(Text, nullable=False)
    # "positive" | "negative"
    type = Column(String(20), nullable=False, default="positive")
    created_at = Column(DateTime, default=_utcnow)

    product = relationship("Product", back_populates="preferences")
