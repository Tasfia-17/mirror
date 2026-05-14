"""Prompt templates for MIRROR agents."""

EMOTION_DETECTION = """Analyze this transcript and detect the primary emotion and tone.

Transcript: {transcript}

Return JSON with:
- emotion: one of [confident, excited, calm, urgent, inspirational, professional]
- tone: one of [casual, formal, energetic, thoughtful]
- key_themes: list of 3 main topics
- speaking_pace: one of [slow, moderate, fast]
- audience: who this message is most relevant to (one sentence)"""

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
    "linkedin": (
        "Professional, value-driven. Start with a bold insight or counterintuitive claim. "
        "Use short paragraphs (1-2 sentences). End with a question to drive comments. "
        "Tone: like a founder on a podcast, honest, no corporate speak. 30-45 sec."
    ),
    "tiktok": (
        "Hook in the first second or you lose them. Fast, punchy sentences. "
        "Use pattern interrupts. Trending audio style. Vertical 9:16. 15-30 sec."
    ),
    "youtube": (
        "Storytelling arc: hook, problem, solution, proof, CTA. "
        "Speak directly to camera. Landscape 16:9. 45-60 sec."
    ),
    "sales": (
        "Problem, Solution, Proof structure. Lead with the pain point. "
        "One clear benefit per sentence. End with a specific CTA. 30 sec."
    ),
    "podcast": (
        "Conversational, deep-dive teaser. Speak as if to one person. "
        "Raise a question you will answer. Audio-first, no visual references. 45-60 sec."
    ),
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
