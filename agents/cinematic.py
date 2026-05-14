"""Cinematic Agent -- B-roll generation via Fal Kling and Wan 2.6."""
import time
from core.state import MirrorState
from clients import fal, posthog_client
from core.prompts import BROLL_PROMPT


SCENE_PROMPTS = [
    "professional walking confidently through a modern office, warm lighting",
    "close-up of hands gesturing while speaking, soft bokeh background",
    "wide establishing shot of a city skyline at golden hour",
    "person looking directly at camera with a slight smile, studio lighting",
]


def run(state: MirrorState) -> MirrorState:
    """Generate cinematic B-roll clips for the primary video format."""
    user_id = state["user_id"]
    face_image_url = state.get("face_image_url")

    broll_urls = []

    # Generate one cinematic multi-shot clip using Kling
    # In production: generate one clip per key scene in the script
    # For demo: generate a single clip to show the capability
    try:
        t0 = time.time()
        url = fal.generate_cinematic(
            prompt=SCENE_PROMPTS[0],
            image_url=face_image_url or "https://via.placeholder.com/512",
            aspect_ratio="16:9",
        )
        duration_ms = (time.time() - t0) * 1000
        broll_urls.append(url)

        posthog_client.track_pipeline(user_id, "cinematic_broll", duration_ms, True, {
            "count": len(broll_urls),
            "trace_id": state.get("trace_id"),
        })
    except Exception as e:
        state["errors"].append(f"cinematic: {e}")
        posthog_client.track_pipeline(user_id, "cinematic_broll", 0, False, {
            "error": str(e),
            "trace_id": state.get("trace_id"),
        })

    state["broll_urls"] = broll_urls
    return state
__all__ = ['run']
