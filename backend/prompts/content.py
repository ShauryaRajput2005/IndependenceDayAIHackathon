"""
prompts/content.py — Dynamic content generation prompt template.
"""

CONTENT_PROMPT_TEMPLATE = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRODUCT INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Name: {product_name}

Category: {category}

Description: {description}

Features:
{features}

Problem solved: {problem}

Target audience: {audience}

Price: {price}

Platform: {platform}

Requested tone: {tone}

Custom requirements:
{requirements}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
USER PREFERENCES (learned from past feedback)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{preferences}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TREND CONTEXT (current formats performing well)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{trends}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MEME FORMATS (available meme vocabulary)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{meme_formats}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOUR TASK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generate a complete short-form viral content package for this product.

The content must:
- Respect the platform ({platform}) and its native conventions
- Match the requested tone exactly ({tone})
- Follow the custom requirements to the letter
- Incorporate relevant trends and meme formats from the context above
- Apply any learned user preferences from past feedback
- Feel authentic, not like an ad

Generate the content now.
"""
