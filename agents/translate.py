"""Translate Agent -- HeyGen Video Translate for 10 languages."""
import time
from core.state import MirrorState
from clients import heygen, posthog_client
from config import LANGUAGES


def run(state: MirrorState) -> MirrorState:
    """Translate primary video to 10 languages."""
    user_id = state["user_id"]
    videos = state["videos"]

    primary_video = videos.get("linkedin")
    if not primary_video:
        state["translations"] = {}
        return state

    # For demo: mock translations so the pipeline runs end-to-end.
    # In production: call heygen.translate_video(primary_video, LANGUAGES)
    # then poll each translation_id with heygen.poll_translation().
    translations = {}
    for lang in LANGUAGES:
        translations[lang] = f"https://mock.heygen.com/translations/{lang}_{user_id}.mp4"

    posthog_client.track_pipeline(user_id, "translate_videos", 0, True, {
        "language_count": len(LANGUAGES),
        "languages": LANGUAGES,
        "source_format": "linkedin",
        "trace_id": state.get("trace_id"),
    })

    state["translations"] = translations
    return state
__all__ = ['run']
