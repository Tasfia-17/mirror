"""Format Agent -- rewrite script for 5 formats + generate videos."""
import time
import json
from openai import OpenAI
from core.state import MirrorState
from clients import posthog_client
from core.prompts import FORMAT_REWRITE, FORMAT_GUIDELINES
from config import OPENAI_API_KEY, FORMATS

_llm = OpenAI(api_key=OPENAI_API_KEY)


def run(state: MirrorState) -> MirrorState:
    """Generate 5 format variations and store scripts for Critic evaluation."""
    user_id = state["user_id"]
    transcript = state["transcript"]
    emotion = state["emotion"]

    state["rewrite_count"] = state.get("rewrite_count", 0) + 1

    scripts = {}
    videos = {}

    for fmt in FORMATS:
        t0 = time.time()
        response = _llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": FORMAT_REWRITE.format(
                format=fmt,
                transcript=transcript,
                emotion=emotion,
                duration=30 if fmt in ["tiktok", "sales"] else 45,
                guidelines=FORMAT_GUIDELINES[fmt],
            )}],
            response_format={"type": "json_object"},
        )
        duration_ms = (time.time() - t0) * 1000

        script_data = json.loads(response.choices[0].message.content)
        script = script_data.get("script", "")
        scripts[fmt] = script

        posthog_client.track_llm(
            user_id, "gpt-4o-mini",
            response.usage.prompt_tokens,
            response.usage.completion_tokens,
            duration_ms, f"format_rewrite_{fmt}",
            trace_id=state.get("trace_id")
        )

        videos[fmt] = f"https://mock.heygen.com/videos/{fmt}_{user_id}.mp4"

        posthog_client.track_pipeline(user_id, f"format_video_{fmt}", duration_ms, True, {
            "format": fmt,
            "script_length": len(script),
            "rewrite_count": state["rewrite_count"],
        })

    state["scripts"] = scripts
    state["videos"] = videos
    return state
