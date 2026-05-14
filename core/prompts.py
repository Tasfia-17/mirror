"""Prompt templates for MIRROR agents."""

EMOTION_DETECTION = """Analyze this transcript and detect the primary emotion and tone.

Transcript: {transcript}

Return JSON with:
- emotion: one of [confident, excited, calm, urgent, inspirational, professional]
- tone: one of [casual, formal, energetic, thoughtful]
- key_themes: list of 3 main topics"""

FORMAT_REWRITE = """Rewrite this transcript for {format} format.

Original transcript: {transcript}
Emotion: {emotion}
Duration target: {duration} seconds

{format} guidelines:
{guidelines}

Return JSON with:
- script: rewritten script optimized for {format}
- hook: first 3 seconds (attention grabber)
- cta: call-to-action"""

FORMAT_GUIDELINES = {
    "linkedin": "Professional, value-driven. Start with insight. End with question to drive comments. 30-45 sec.",
    "tiktok": "Hook in 1 sec. Fast cuts. Trending audio style. Vertical 9:16. 15-30 sec.",
    "youtube": "Storytelling arc. Intro/body/CTA. Landscape 16:9. 45-60 sec.",
    "sales": "Problem, Solution, Proof. Direct, benefit-focused. 30 sec.",
    "podcast": "Conversational, deep-dive teaser. Audio-first. 45-60 sec.",
}

BROLL_PROMPT = """Generate a B-roll scene description for this moment:

Script segment: {segment}
Emotion: {emotion}
Format: {format}

Return a single cinematic scene description (no camera directions, just visual action)."""

THUMBNAIL_PROMPT = """Create a thumbnail image prompt for this video:

Title: {title}
Format: {format}
Emotion: {emotion}

Return a FLUX prompt for an eye-catching thumbnail (no text, pure visual)."""
