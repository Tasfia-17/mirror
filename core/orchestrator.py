"""MIRROR Orchestrator -- LangGraph state machine with conditional edges and router visualization."""
import time
import uuid
from langgraph.graph import StateGraph, END
from core.state import MirrorState
from agents import intake, identity, format, critic, cinematic, hyperframes, translate, optimizer
from clients import posthog_client
from core.router_viz import get_router_viz, reset_router_viz


def route_by_quality(state: MirrorState) -> str:
    """Route based on critic scores. Loop back to format if any score < 7/10."""
    scores = state.get("quality_scores", {})
    if not scores:
        return "proceed"

    min_score = min(scores.values())
    rewrite_count = state.get("rewrite_count", 0)

    if min_score < 7.0 and rewrite_count < 2:
        return "rewrite"
    return "proceed"


def create_graph():
    """Build the MIRROR pipeline graph with conditional edges."""
    workflow = StateGraph(MirrorState)

    workflow.add_node("intake", intake.run)
    workflow.add_node("identity", identity.run)
    workflow.add_node("format", format.run)
    workflow.add_node("critic", critic.run)
    workflow.add_node("cinematic", cinematic.run)
    workflow.add_node("hyperframes", hyperframes.run)
    workflow.add_node("translate", translate.run)
    workflow.add_node("optimizer", optimizer.run)

    workflow.set_entry_point("intake")
    workflow.add_edge("intake", "identity")
    workflow.add_edge("identity", "format")
    workflow.add_edge("format", "critic")

    workflow.add_conditional_edges(
        "critic",
        route_by_quality,
        {
            "rewrite": "format",
            "proceed": "cinematic",
        }
    )

    workflow.add_edge("cinematic", "hyperframes")
    workflow.add_edge("hyperframes", "translate")
    workflow.add_edge("translate", "optimizer")
    workflow.add_edge("optimizer", END)

    return workflow.compile()


def run_pipeline(audio_path: str, user_id: str = None) -> dict:
    """Execute the full MIRROR pipeline."""
    if not user_id:
        user_id = str(uuid.uuid4())[:8]

    trace_id = str(uuid.uuid4())
    start_time = time.time()

    initial_state: MirrorState = {
        "user_id": user_id,
        "audio_path": audio_path,
        "trace_id": trace_id,
        "transcript": None,
        "language": None,
        "emotion": None,
        "voice_id": None,
        "avatar_id": None,
        "avatar_look_id": None,
        "face_image_url": None,
        "scripts": {},
        "videos": {},
        "broll_urls": [],
        "translations": {},
        "quality_scores": None,
        "rewrite_count": 0,
        "optimized_prompts": None,
        "liveavatar_session": None,
        "errors": [],
        "start_time": start_time,
    }

    posthog_client.capture(user_id, "mirror_pipeline_start", {
        "audio_path": audio_path,
        "trace_id": trace_id,
    })

    try:
        graph = create_graph()
        final_state = graph.invoke(initial_state)

        total_duration = time.time() - start_time

        posthog_client.capture(user_id, "mirror_pipeline_complete", {
            "duration_seconds": total_duration,
            "video_count": len(final_state["videos"]),
            "translation_count": len(final_state["translations"]),
            "total_outputs": len(final_state["videos"]) + len(final_state["translations"]),
            "quality_scores": final_state.get("quality_scores"),
            "rewrite_count": final_state.get("rewrite_count", 0),
            "trace_id": trace_id,
        })

        posthog_client.flush()

        return {
            "user_id": user_id,
            "trace_id": trace_id,
            "duration_seconds": total_duration,
            "transcript": final_state["transcript"],
            "emotion": final_state["emotion"],
            "scripts": final_state["scripts"],
            "videos": final_state["videos"],
            "translations": final_state["translations"],
            "quality_scores": final_state.get("quality_scores"),
            "total_outputs": len(final_state["videos"]) + len(final_state["translations"]),
            "errors": final_state["errors"],
        }
    except Exception as e:
        posthog_client.capture(user_id, "mirror_pipeline_error", {
            "error": str(e),
            "error_type": type(e).__name__,
            "trace_id": trace_id,
        })
        posthog_client.flush()
        raise
__all__ = ['run_pipeline', 'create_graph']
