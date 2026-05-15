"""Central configuration with lazy environment variable validation."""
import os
from dotenv import load_dotenv

load_dotenv()


def _require(key: str) -> str:
    """Get required env var or raise with a helpful message."""
    val = os.getenv(key)
    if not val:
        raise EnvironmentError(
            f"Missing required environment variable: {key}\n"
            f"Copy .env.example to .env and add your API keys.\n"
            f"See QUICKSTART.md for setup instructions."
        )
    return val


def _lazy(key: str, default: str = "") -> str:
    """Get env var lazily — returns empty string if missing (for test imports)."""
    return os.getenv(key, default)


ELEVENLABS_API_KEY = _lazy("ELEVENLABS_API_KEY")
HEYGEN_API_KEY = _lazy("HEYGEN_API_KEY")
FAL_KEY = _lazy("FAL_KEY")
POSTHOG_API_KEY = _lazy("POSTHOG_API_KEY")
POSTHOG_HOST = os.getenv("POSTHOG_HOST", "https://app.posthog.com")
OPENAI_API_KEY = _lazy("OPENROUTER_API_KEY")  # OpenRouter key
OPENAI_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENAI_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
DEV_MODE = os.getenv("ENV") == "dev"

HEYGEN_BASE = "https://api.heygen.com"
HEYGEN_HEADERS = {"X-Api-Key": HEYGEN_API_KEY, "Content-Type": "application/json"}

FORMATS = ["linkedin", "tiktok", "youtube", "sales", "podcast"]
LANGUAGES = [
    "Spanish", "French", "German", "Japanese", "Chinese",
    "Portuguese", "Korean", "Arabic", "Hindi", "Italian",
]

# Version
VERSION = "1.0.0"

# Feature flags
ENABLE_CRITIC_LOOP = True
ENABLE_HYPERFRAMES = True
ENABLE_TRANSLATIONS = True

# Demo mode: pre-approve all Critic scores for reliable demo timing
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"
