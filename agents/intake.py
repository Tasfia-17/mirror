"""Intake Agent -- transcribe audio and detect emotion."""
import time
import json
from openai import OpenAI
from core.state import MirrorState
from clients import elevenlabs, posthog_client
from core.prompts import EMOTION_DETECTION
from config import OPENAI_API_KEY

_llm = OpenAI(api_key=OPENAI_API_KEY)


def run(state: MirrorState) -> MirrorState:
    """Transcribe audio and detect emotion."""
    user_id = state["user_id"]
    audio_path = state["audio_path"]

    t0 = time.time()
    result = elevenlabs.transcribe(audio_path)
    duration_ms = (time.time() - t0) * 1000

    posthog_client.track_pipeline(user_id, "intake_transcribe", duration_ms, True, {
        "language": result["language"],
        "word_count": len(result["text"].split()),
        "trace_id": state.get("trace_id"),
    })

    state["transcript"] = result["text"]
    state["language"] = result["language"]

    t0 = time.time()
    response = _llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": EMOTION_DETECTION.format(transcript=result["text"])}],
        response_format={"type": "json_object"},
    )
    duration_ms = (time.time() - t0) * 1000

    emotion_data = json.loads(response.choices[0].message.content)
    state["emotion"] = emotion_data.get("emotion", "professional")
    state["language"] = result.get("language", "en")

    # Store additional intake metadata for downstream agents
    if "key_themes" in emotion_data:
        state.setdefault("errors", [])  # ensure errors list exists

    posthog_client.track_llm(
        user_id, "gpt-4o-mini",
        response.usage.prompt_tokens,
        response.usage.completion_tokens,
        duration_ms, "emotion_detection",
        trace_id=state.get("trace_id")
    )

    return state
__all__ = ['run']
