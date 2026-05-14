"""Vision Agent -- analyze visual context from uploaded images or video frames."""
import base64
from openai import OpenAI
from core.state import MirrorState
from clients import posthog_client
from config import OPENAI_API_KEY

_llm = OpenAI(api_key=OPENAI_API_KEY)

__all__ = ["run", "analyze_image"]


def analyze_image(image_path: str) -> dict:
    """Analyze an image using GPT-4 Vision. Returns scene description and context."""
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    response = _llm.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": "Analyze this image. Describe: 1) Main subject, 2) Setting/environment, 3) Mood/emotion, 4) Key visual elements. Return JSON."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
            ]
        }],
        response_format={"type": "json_object"},
        max_tokens=300,
    )

    import json
    return json.loads(response.choices[0].message.content)


def run(state: MirrorState) -> MirrorState:
    """Analyze visual context if image_path is provided in state."""
    user_id = state["user_id"]
    image_path = state.get("image_path")

    if not image_path:
        return state

    try:
        import time
        t0 = time.time()
        analysis = analyze_image(image_path)
        duration_ms = (time.time() - t0) * 1000

        state["visual_context"] = analysis

        posthog_client.track_pipeline(user_id, "vision_analyze", duration_ms, True, {
            "has_subject": "subject" in analysis,
            "trace_id": state.get("trace_id"),
        })
    except Exception as e:
        state.setdefault("errors", []).append(f"vision: {e}")
        posthog_client.track_pipeline(user_id, "vision_analyze", 0, False, {
            "error": str(e),
            "trace_id": state.get("trace_id"),
        })

    return state
