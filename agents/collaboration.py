"""Avatar Collaboration Agent -- theatrical demo moment where two avatars communicate via visual protocol."""
import json
from openai import OpenAI
from core.state import MirrorState
from clients import posthog_client
from config import OPENAI_API_KEY

_llm = OpenAI(api_key=OPENAI_API_KEY)

__all__ = ["run", "create_visual_markup"]


def create_visual_markup(script: str, feedback: str) -> dict:
    """Generate Hyperframes visual markup for avatar-to-avatar communication."""
    prompt = f"""Two AI avatars are collaborating on a script. Avatar 2 is reviewing Avatar 1's work.

Original script: {script}

Feedback: {feedback}

Generate visual markup annotations (circles, arrows, highlights) that Avatar 2 would use to communicate changes.
Return JSON with: {{"annotations": [{{"type": "circle", "text": "weak hook", "position": "top"}}, ...], "approved": false}}"""

    response = _llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        max_tokens=300,
    )
    
    return json.loads(response.choices[0].message.content)


def run(state: MirrorState) -> MirrorState:
    """Demonstrate avatar collaboration via visual protocol."""
    user_id = state["user_id"]
    scripts = state.get("scripts", {})
    
    if not scripts or "linkedin" not in scripts:
        return state
    
    # Simulate Avatar 1 proposing script
    linkedin_script = scripts["linkedin"]
    
    # Avatar 2 reviews via visual markup
    feedback = "Hook needs more impact. CTA should be more specific."
    markup = create_visual_markup(linkedin_script, feedback)
    
    # Store collaboration data for demo visualization
    state["avatar_collaboration"] = {
        "original_script": linkedin_script,
        "visual_markup": markup,
        "protocol": "hyperframes_visual",
        "speed_improvement": "10x faster than speech",
    }
    
    posthog_client.capture(user_id, "avatar_collaboration", {
        "annotations_count": len(markup.get("annotations", [])),
        "approved": markup.get("approved", False),
        "trace_id": state.get("trace_id"),
    })
    
    return state
