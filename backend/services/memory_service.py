from database.database import execute, fetch_all


def get_memory(product_id: int) -> str:
    rows = fetch_all(
        """
        SELECT preference, type
        FROM preferences
        WHERE product_id = ?
        ORDER BY created_at DESC, id DESC
        LIMIT 8
        """,
        (product_id,),
    )
    if not rows:
        return "No previous preferences yet."

    positive = [row["preference"] for row in rows if row["type"].lower() == "positive"]
    negative = [row["preference"] for row in rows if row["type"].lower() != "positive"]

    lines: list[str] = []
    if positive:
        lines.append("User prefers:")
        lines.extend(f"- {item}" for item in positive)
    if negative:
        lines.append("Avoid:")
        lines.extend(f"- {item}" for item in negative)
    return "\n".join(lines)


def add_preference(product_id: int, preference: str, preference_type: str = "Positive") -> int:
    return execute(
        """
        INSERT INTO preferences (product_id, preference, type)
        VALUES (?, ?, ?)
        """,
        (product_id, preference, preference_type),
    )


def feedback_to_preference(feedback: str) -> tuple[str, str]:
    normalized = feedback.strip()
    lowered = normalized.lower()
    negative_markers = ["avoid", "less", "not", "too formal", "bad", "boring"]
    preference_type = "Negative" if any(marker in lowered for marker in negative_markers) else "Positive"
    return normalized, preference_type
