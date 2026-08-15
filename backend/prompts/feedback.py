"""
prompts/feedback.py — Prompt template for LLM-based preference extraction.
Used ONLY for free-text comments that don't map to a known feedback_type.
"""

FEEDBACK_EXTRACTION_PROMPT = """
A user left the following comment about AI-generated social media content:

"{comment}"

Extract a single, concise content preference from this comment (max 10 words).
Classify it as either "positive" (what to do more of) or "negative" (what to avoid).

Examples:
- "Make it funnier" → positive: "humorous and witty content"
- "Too corporate" → negative: "corporate and formal language"
- "Love the Hinglish" → positive: "Hinglish language and desi references"

Respond with exactly:
preference: <preference text>
type: <positive|negative>
"""
