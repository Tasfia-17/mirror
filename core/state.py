"""Shared state for MIRROR pipeline."""
from typing import TypedDict, Optional


class MirrorState(TypedDict):
    # Input
    user_id: str
    audio_path: str
    image_path: Optional[str]  # Optional image for visual context
    trace_id: Optional[str]

    # Intake outputs
    transcript: Optional[str]
    language: Optional[str]
    emotion: Optional[str]

    # Vision outputs
    visual_context: Optional[dict]  # Scene description from image analysis

    # Identity outputs
    voice_id: Optional[str]
    avatar_id: Optional[str]
    avatar_look_id: Optional[str]
    face_image_url: Optional[str]

    # Format outputs
    scripts: dict        # {format: script_text}
    videos: dict         # {format: video_url}

    # Cinematic outputs
    broll_urls: list

    # Translate outputs
    translations: dict   # {language: video_url}

    # Critic outputs
    quality_scores: Optional[dict]   # {platform: score}
    rewrite_count: int

    # Optimizer outputs
    optimized_prompts: Optional[dict]

    # Avatar collaboration
    avatar_collaboration: Optional[dict]

    # LiveAvatar session
    liveavatar_session: Optional[dict]

    # Metadata
    errors: list
    start_time: float
__all__ = ['MirrorState']


def validate_state(state: MirrorState) -> bool:
    """Validate that required state fields are present."""
    required = ["user_id", "audio_path"]
    return all(state.get(k) for k in required)
