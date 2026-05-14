"""Central configuration loader for MIRROR."""
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
            f"See README.md for setup instructions."
        )
    return val


ELEVENLABS_API_KEY = _require("ELEVENLABS_API_KEY")
HEYGEN_API_KEY = _require("HEYGEN_API_KEY")
FAL_KEY = _require("FAL_KEY")
POSTHOG_API_KEY = _require("POSTHOG_API_KEY")
POSTHOG_HOST = os.getenv("POSTHOG_HOST", "https://app.posthog.com")
OPENAI_API_KEY = _require("OPENAI_API_KEY")
DEV_MODE = os.getenv("ENV") == "dev"

HEYGEN_BASE = "https://api.heygen.com"
HEYGEN_HEADERS = {"X-Api-Key": HEYGEN_API_KEY, "Content-Type": "application/json"}

FORMATS = ["linkedin", "tiktok", "youtube", "sales", "podcast"]
LANGUAGES = [
    "Spanish", "French", "German", "Japanese", "Chinese",
    "Portuguese", "Korean", "Arabic", "Hindi", "Italian",
]
