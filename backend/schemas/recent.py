from typing import Any

from pydantic import BaseModel


class RecentGeneration(BaseModel):
    generation_id: int
    product_id: int
    product_name: str
    tone: str
    response: dict[str, Any]
    created_at: str
