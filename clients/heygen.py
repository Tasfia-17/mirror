"""HeyGen client -- Avatar V, Video Agent, Video Translate, polling."""
import time
import requests
from config import HEYGEN_BASE, HEYGEN_HEADERS, HEYGEN_API_KEY
from core.retry import with_retry


def _get(path: str) -> dict:
    r = requests.get(f"{HEYGEN_BASE}{path}", headers=HEYGEN_HEADERS, timeout=30)
    r.raise_for_status()
    data = r.json()
    if "data" not in data:
        raise RuntimeError(f"HeyGen API error: {data.get('message', 'Unknown error')}")
    return data["data"]


def _post(path: str, json: dict) -> dict:
    r = requests.post(f"{HEYGEN_BASE}{path}", headers=HEYGEN_HEADERS, json=json, timeout=30)
    r.raise_for_status()
    data = r.json()
    if "data" not in data:
        raise RuntimeError(f"HeyGen API error: {data.get('message', 'Unknown error')}")
    return data["data"]


def upload_asset(file_path: str) -> str:
    """Upload file to HeyGen assets. Returns asset_id."""
    with open(file_path, "rb") as f:
        r = requests.post(
            f"{HEYGEN_BASE}/v3/assets",
            headers={"X-Api-Key": HEYGEN_API_KEY},
            files={"file": f},
            timeout=60,
        )
    r.raise_for_status()
    return r.json()["data"]["asset_id"]


def create_avatar_v(video_asset_id: str, name: str = "mirror_twin") -> dict:
    """Create Avatar V digital twin. Returns avatar data."""
    return _post("/v3/avatars", {
        "type": "digital_twin",
        "name": name,
        "file": {"type": "asset_id", "asset_id": video_asset_id},
    })


@with_retry(max_attempts=3, base_delay=2.0)
def poll_avatar(look_id: str, timeout: int = 300) -> str:
    """Poll avatar look until completed. Returns look_id."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        data = _get(f"/v3/avatars/looks/{look_id}")
        status = data.get("status")
        if status == "completed":
            return look_id
        if status == "failed":
            raise RuntimeError(f"Avatar training failed for {look_id}")
        time.sleep(10)
    raise TimeoutError(f"Avatar {look_id} not ready after {timeout}s")


def create_video_agent(prompt: str, avatar_id: str = None, voice_id: str = None,
                       orientation: str = "landscape", files: list = None) -> dict:
    """Create video via Video Agent. Returns {session_id, video_id}."""
    payload = {"prompt": prompt, "orientation": orientation, "mode": "generate"}
    if avatar_id:
        payload["avatar_id"] = avatar_id
    if voice_id:
        payload["voice_id"] = voice_id
    if files:
        payload["files"] = files
    return _post("/v3/video-agents", payload)


def create_video_direct(avatar_id: str, script: str, voice_id: str,
                        orientation: str = "landscape") -> dict:
    """Create video with explicit params using Avatar V engine."""
    aspect = "16:9" if orientation == "landscape" else "9:16"
    return _post("/v3/videos", {
        "type": "avatar",
        "avatar_id": avatar_id,
        "script": script,
        "voice_id": voice_id,
        "aspect_ratio": aspect,
        "resolution": "1080p",
        "engine": {"type": "avatar_v"},
    })


@with_retry(max_attempts=3, base_delay=2.0)
def poll_video(video_id: str, timeout: int = 600) -> dict:
    """Poll video until completed or failed. Returns full video data."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        data = _get(f"/v3/videos/{video_id}")
        if data["status"] == "completed":
            return data
        if data["status"] == "failed":
            raise RuntimeError(f"Video {video_id} failed: {data.get('failure_message')}")
        time.sleep(15)
    raise TimeoutError(f"Video {video_id} not ready after {timeout}s")


def poll_session_video(session_id: str, timeout: int = 600) -> str:
    """Poll Video Agent session until video_id is assigned. Returns video_id."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        data = _get(f"/v3/video-agents/{session_id}")
        if data.get("video_id"):
            return data["video_id"]
        if data.get("status") == "failed":
            raise RuntimeError(f"Session {session_id} failed")
        time.sleep(10)
    raise TimeoutError(f"Session {session_id} no video_id after {timeout}s")


def translate_video(video_url: str, languages: list, mode: str = "speed") -> list:
    """Translate video to multiple languages. Returns list of translation_ids."""
    data = _post("/v3/video-translations", {
        "video": {"type": "url", "url": video_url},
        "output_languages": languages,
        "mode": mode,
        "enable_caption": True,
    })
    return data.get("video_translation_ids", [])


@with_retry(max_attempts=3, base_delay=2.0)
def poll_translation(translation_id: str, timeout: int = 600) -> dict:
    """Poll translation until completed. Returns translation data."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        data = _get(f"/v3/video-translations/{translation_id}")
        if data["status"] == "completed":
            return data
        if data["status"] == "failed":
            raise RuntimeError(f"Translation {translation_id} failed")
        time.sleep(15)
    raise TimeoutError(f"Translation {translation_id} not ready after {timeout}s")
__all__ = ['create_avatar_v', 'create_video_agent', 'translate_video', 'poll_video']
