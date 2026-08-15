"""
schemas/recent.py — Response schema for the recent generations list.
"""
from datetime import datetime
from typing import List

from pydantic import BaseModel


class RecentGenerationItem(BaseModel):
    id: int
    product_id: int
    hook: str
    tone: str
    platform: str
    created_at: datetime

    model_config = {"from_attributes": True}


class RecentGenerationsResponse(BaseModel):
    items: List[RecentGenerationItem]
    total: int
