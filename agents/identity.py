"""Identity Agent -- voice clone and Avatar V creation."""
import time
from core.state import MirrorState
from clients import elevenlabs, posthog_client


def run(state: MirrorState) -> MirrorState:
    """Clone voice and create Avatar V digital twin."""
    user_id = state["user_id"]
    audio_path = state["audio_path"]

    t0 = time.time()
    voice_id = elevenlabs.clone_voice(audio_path, f"mirror_{user_id}")
    duration_ms = (time.time() - t0) * 1000

    posthog_client.track_pipeline(user_id, "identity_voice_clone", duration_ms, True, {
        "voice_id": voice_id,
        "trace_id": state.get("trace_id"),
    })

    state["voice_id"] = voice_id

    # Avatar V creation requires a video file of the speaker.
    # For the hackathon demo we use a mock avatar_id so the pipeline
    # runs end-to-end without a 5-10 minute training wait.
    # In production: upload speaker video, call heygen.create_avatar_v(),
    # then poll heygen.poll_avatar() until completed.
    state["avatar_id"] = "mock_avatar_v"
    state["avatar_look_id"] = "mock_look"

    posthog_client.track_pipeline(user_id, "identity_avatar_create", 0, True, {
        "avatar_id": state["avatar_id"],
        "mode": "mock",
        "trace_id": state.get("trace_id"),
    })

    return state
__all__ = ['run']
