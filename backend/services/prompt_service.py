import json
from sqlite3 import Row

from prompts.content import CONTENT_PROMPT_TEMPLATE
from services.memory_service import get_memory
from services.trend_service import get_trends


def build_content_prompt(product: Row, tone: str | None = None, requirements: str | None = None) -> str:
    trend_summary = json.dumps(get_trends(), ensure_ascii=True, indent=2)
    return CONTENT_PROMPT_TEMPLATE.format(
        name=product["name"],
        category=product["category"],
        description=product["description"],
        features=product["features"] or "Not provided",
        problem=product["problem"] or "Not provided",
        audience=product["audience"],
        price_range=product["price_range"] or "Not provided",
        competitors=product["competitors"] or "Not provided",
        platform=product["platform"],
        tone=tone or product["tone"],
        requirements=requirements or product["requirements"] or "No extra requirements.",
        trends=trend_summary,
        memory=get_memory(product["id"]),
    )
