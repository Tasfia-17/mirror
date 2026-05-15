"""Optimizer Agent -- PostHog query and prompt improvement."""
from core.state import MirrorState
from clients import posthog_client
from core.self_improvement import get_improvement_demo


def run(state: MirrorState) -> MirrorState:
    """Query PostHog for performance data and surface optimization signals."""
    user_id = state["user_id"]
    quality_scores = state.get("quality_scores", {})

    optimized = {}
    if quality_scores:
        weakest = min(quality_scores, key=quality_scores.get)
        optimized["focus_format"] = weakest
        optimized["min_score"] = quality_scores[weakest]
        optimized["avg_score"] = round(sum(quality_scores.values()) / len(quality_scores), 2)

        # Run self-improvement demo
        improvement = get_improvement_demo().simulate_improvement(user_id, quality_scores)
        optimized["improvement"] = improvement

    state["optimized_prompts"] = optimized

    posthog_client.track_pipeline(user_id, "optimizer_analyze", 0, True, {
        "quality_scores": quality_scores,
        "optimized": {k: v for k, v in optimized.items() if k != "improvement"},
        "trace_id": state.get("trace_id"),
    })

    return state
__all__ = ['run']
