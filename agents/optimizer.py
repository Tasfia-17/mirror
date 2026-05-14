"""Optimizer Agent -- PostHog query and prompt improvement."""
from core.state import MirrorState
from clients import posthog_client


def run(state: MirrorState) -> MirrorState:
    """Query PostHog for performance data and surface optimization signals."""
    user_id = state["user_id"]
    quality_scores = state.get("quality_scores", {})

    # Identify the weakest format so the next run can prioritize it
    optimized = {}
    if quality_scores:
        weakest = min(quality_scores, key=quality_scores.get)
        optimized["focus_format"] = weakest
        optimized["min_score"] = quality_scores[weakest]
        optimized["avg_score"] = round(sum(quality_scores.values()) / len(quality_scores), 2)

    state["optimized_prompts"] = optimized

    posthog_client.track_pipeline(user_id, "optimizer_analyze", 0, True, {
        "quality_scores": quality_scores,
        "optimized": optimized,
        "trace_id": state.get("trace_id"),
    })

    return state
__all__ = ['run']
