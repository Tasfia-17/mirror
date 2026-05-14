"""Critic Agent -- Quality gate before expensive video generation."""
import json
from openai import OpenAI
from core.state import MirrorState
from clients import posthog_client
from config import OPENAI_API_KEY, DEMO_MODE

_llm = OpenAI(api_key=OPENAI_API_KEY)

SCRIPT_RUBRIC = """Evaluate this {platform} script on a 0-10 scale.

Script:
{script}

Criteria:
1. Hook strength (first 3 seconds grab attention)
2. CTA clarity (call-to-action is specific and actionable)
3. Emotional resonance (matches detected emotion: {emotion})
4. Platform fit (optimized for {platform} audience)

Return JSON: {{"hook": 8, "cta": 7, "emotion": 9, "platform": 8, "overall": 8.0}}"""


def run(state: MirrorState) -> MirrorState:
    """Evaluate script quality before expensive video generation."""
    user_id = state["user_id"]
    scripts = state.get("scripts", {})
    emotion = state.get("emotion", "professional")

    if not scripts:
        state["quality_scores"] = {}
        return state

    # Demo mode: approve all scripts immediately for reliable timing
    if DEMO_MODE:
        scores = {platform: 8.5 for platform in scripts.keys()}
        state["quality_scores"] = scores
        for platform in scripts.keys():
            posthog_client.capture(user_id, "critic_evaluation", {
                "platform": platform,
                "score": 8.5,
                "demo_mode": True,
                "trace_id": state.get("trace_id"),
            })
        return state

    scores = {}

    for platform, script in scripts.items():
        prompt = SCRIPT_RUBRIC.format(
            platform=platform,
            script=script,
            emotion=emotion,
        )

        response = _llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )

        score_data = json.loads(response.choices[0].message.content)
        overall = score_data.get("overall", 5.0)
        scores[platform] = overall

        posthog_client.capture(user_id, "critic_evaluation", {
            "platform": platform,
            "score": overall,
            "hook_score": score_data.get("hook"),
            "cta_score": score_data.get("cta"),
            "emotion_score": score_data.get("emotion"),
            "platform_score": score_data.get("platform"),
            "rewrite_count": state.get("rewrite_count", 0),
            "trace_id": state.get("trace_id"),
        })

    state["quality_scores"] = scores
    return state
__all__ = ['run']
