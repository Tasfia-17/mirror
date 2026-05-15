"""LiveAvatar Agent -- Real-time interaction with the speaker's digital twin."""
import requests
from openai import OpenAI
from core.state import MirrorState
from clients import posthog_client
from config import HEYGEN_API_KEY, HEYGEN_BASE, HEYGEN_HEADERS, OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL

_llm = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)


def create_session(state: MirrorState) -> dict:
    """Create a HeyGen LiveAvatar session in LITE mode."""
    context = (
        f"You are the digital twin of user {state['user_id']}. "
        f"Original transcript: {state.get('transcript', '')}. "
        f"Detected emotion: {state.get('emotion', 'professional')}. "
        f"Formats created: {', '.join(state.get('videos', {}).keys())}. "
        f"Languages: 10 (Spanish, French, German, Japanese, Chinese, "
        f"Portuguese, Korean, Arabic, Hindi, Italian). "
        f"Answer questions about the content generation process or the original message."
    )

    payload = {
        "avatar_id": state.get("avatar_id", "mock_avatar_v"),
        "voice": {
            "type": "elevenlabs",
            "voice_id": state.get("voice_id", ""),
        },
        "mode": "LITE",
        "context": context,
    }

    try:
        r = requests.post(
            f"{HEYGEN_BASE}/v1/streaming.new",
            headers=HEYGEN_HEADERS,
            json=payload,
            timeout=30,
        )
        r.raise_for_status()
        data = r.json()
        session_id = data.get("session_id")

        posthog_client.capture(state["user_id"], "liveavatar_session_created", {
            "session_id": session_id,
            "trace_id": state.get("trace_id"),
        })

        return {
            "session_id": session_id,
            "room_url": f"https://app.heygen.com/streaming/{session_id}",
            "status": "ready",
        }
    except Exception as e:
        return {
            "session_id": "fallback",
            "room_url": None,
            "status": "fallback",
            "error": str(e),
        }


def answer_question(question: str, state: MirrorState) -> str:
    """Generate a contextual answer using the pipeline state as context."""
    context = (
        f"Original transcript: {state.get('transcript', '')}\n"
        f"Emotion detected: {state.get('emotion', 'professional')}\n"
        f"Formats generated: {len(state.get('videos', {}))}\n"
        f"Languages: {len(state.get('translations', {}))}\n"
        f"Quality scores: {state.get('quality_scores', {})}"
    )

    response = _llm.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": f"You are the user's digital twin.\n{context}"},
            {"role": "user", "content": question},
        ],
        max_tokens=150,
    )
    return response.choices[0].message.content


def run(state: MirrorState) -> MirrorState:
    """Create LiveAvatar session and attach to state."""
    session = create_session(state)
    state["liveavatar_session"] = session
    return state
__all__ = ['create_session', 'answer_question', 'run']
