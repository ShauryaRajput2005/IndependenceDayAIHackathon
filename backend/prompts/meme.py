"""
prompts/meme.py — Meme context formatting helpers.
"""


def format_meme_context(meme_formats: list) -> str:
    """Convert meme format dicts into a readable block for the prompt."""
    if not meme_formats:
        return "No meme formats loaded."

    lines = []
    for fmt in meme_formats:
        name = fmt.get("name", "Unknown")
        desc = fmt.get("description", "")
        best_for = fmt.get("best_for", [])
        if isinstance(best_for, list):
            best_for = ", ".join(best_for)
        queries = fmt.get("search_queries", [])
        query_str = ", ".join(queries[:2]) if queries else ""
        lines.append(f"• {name}: {desc}")
        if best_for:
            lines.append(f"  Best for: {best_for}")
        if query_str:
            lines.append(f"  GIF search: {query_str}")
    return "\n".join(lines)
