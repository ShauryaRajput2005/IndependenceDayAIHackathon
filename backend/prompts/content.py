CONTENT_PROMPT_TEMPLATE = """
Product Information:
Name: {name}
Category: {category}
Description: {description}
Features: {features}
Problem Solved: {problem}
Audience: {audience}
Price Range: {price_range}
Competitors: {competitors}
Platform: {platform}

Requested Tone: {tone}
User Requirements: {requirements}

Curated Trends:
{trends}

Previous User Preferences:
{memory}

Return only this JSON shape:
{{
  "hook": "string",
  "meme_format": "string",
  "dialogue": ["string", "string"],
  "script": [{{"scene": "string", "time": "0-3 sec"}}],
  "caption": "string",
  "klipy_query": "string",
  "hashtags": ["#tag"],
  "viral_score": 0
}}
""".strip()
