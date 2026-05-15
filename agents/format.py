"""Format Agent -- rewrite script for 5 platforms with async parallelization."""
import time
import json
import asyncio
from openai import OpenAI, AsyncOpenAI
from core.state import MirrorState
from clients import posthog_client
from core.prompts import FORMAT_REWRITE, FORMAT_GUIDELINES
from config import OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL, FORMATS

_llm = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
_async_llm = AsyncOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)


async def _rewrite_format(fmt: str, transcript: str, emotion: str) -> tuple:
    """Rewrite transcript for a single format. Returns (fmt, script_data)."""
    response = await _async_llm.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": FORMAT_REWRITE.format(
            format=fmt,
            transcript=transcript,
            emotion=emotion,
            duration=30 if fmt in ["tiktok", "sales"] else 45,
            guidelines=FORMAT_GUIDELINES[fmt],
        )}],
        response_format={"type": "json_object"},
    )
    script_data = json.loads(response.choices[0].message.content)
    usage = response.usage
    return fmt, script_data, usage


async def _run_async(transcript: str, emotion: str, formats: list) -> dict:
    """Run all format rewrites in parallel."""
    tasks = [_rewrite_format(fmt, transcript, emotion) for fmt in formats]
    results = await asyncio.gather(*tasks)
    return {fmt: (data, usage) for fmt, data, usage in results}


def run(state: MirrorState) -> MirrorState:
    """Generate 5 format variations in parallel and store scripts in state."""
    user_id = state["user_id"]
    transcript = state["transcript"]
    emotion = state["emotion"]

    state["rewrite_count"] = state.get("rewrite_count", 0) + 1

    t0 = time.time()
    results = asyncio.run(_run_async(transcript, emotion, state.get("formats", FORMATS)))
    total_ms = (time.time() - t0) * 1000

    scripts = {}
    videos = {}

    for fmt, (script_data, usage) in results.items():
        script = script_data.get("script", "")
        scripts[fmt] = script
        videos[fmt] = f"https://mock.heygen.com/videos/{fmt}_{user_id}.mp4"

        posthog_client.track_llm(
            user_id, "gpt-4o-mini",
            usage.prompt_tokens,
            usage.completion_tokens,
            total_ms / len(FORMATS), f"format_rewrite_{fmt}",
            trace_id=state.get("trace_id")
        )

        posthog_client.track_pipeline(user_id, f"format_video_{fmt}", total_ms / len(FORMATS), True, {
            "format": fmt,
            "script_length": len(script),
            "rewrite_count": state["rewrite_count"],
        })

    state["scripts"] = scripts
    state["videos"] = videos
    return state
__all__ = ['run']
