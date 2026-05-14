"""PostHog client -- event capture, LLM tracing, prompt management."""
from posthog import Posthog
from config import POSTHOG_API_KEY, POSTHOG_HOST

_client = Posthog(project_api_key=POSTHOG_API_KEY or "test", host=POSTHOG_HOST)
_client.debug = False


def capture(user_id: str, event: str, props: dict = None):
    _client.capture(user_id, event, properties=props or {})


def track_llm(user_id: str, model: str, input_tokens: int, output_tokens: int,
              latency_ms: float, step: str, cost_usd: float = 0.0, trace_id: str = None):
    """Track LLM call with PostHog AI observability properties."""
    _client.capture(user_id, "$ai_generation", properties={
        "$ai_model": model,
        "$ai_provider": "openai" if "gpt" in model else "anthropic",
        "$ai_input_tokens": input_tokens,
        "$ai_output_tokens": output_tokens,
        "$ai_latency": latency_ms / 1000,
        "$ai_total_cost_usd": cost_usd,
        "$ai_trace_id": trace_id,
        "step": step,
    })


def track_pipeline(user_id: str, step: str, duration_ms: float,
                   success: bool, meta: dict = None):
    """Track a pipeline step with timing and success status."""
    _client.capture(user_id, "mirror_pipeline_step", properties={
        "step": step,
        "duration_ms": duration_ms,
        "success": success,
        **(meta or {}),
    })


def flush():
    _client.flush()


def fetch_prompt(agent_name: str, user_id: str, default: str) -> str:
    """Fetch prompt variant from PostHog feature flags for runtime A/B testing."""
    prompt = _client.get_feature_flag(f"prompt_{agent_name}", user_id)
    return prompt if prompt else default


def evaluate_output(trace_id: str, agent: str, output: str, criterion: str, score: float):
    """Track agent output evaluation score for PostHog analytics."""
    _client.capture(trace_id, "agent_evaluation", properties={
        "agent": agent,
        "criterion": criterion,
        "score": score,
        "output_length": len(output),
    })


__all__ = ['capture', 'track_llm', 'track_pipeline', 'flush']
