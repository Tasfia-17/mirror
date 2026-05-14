"""Fal.ai client -- Wan 2.6 R2V, Kling cinematic, FLUX thumbnail."""
import os
import fal_client
from config import FAL_KEY

os.environ["FAL_KEY"] = FAL_KEY


def generate_broll(prompt: str, video_url: str = None, image_url: str = None,
                   aspect_ratio: str = "16:9", duration: str = "5") -> str:
    """Generate B-roll via Wan 2.6 R2V. Returns video URL."""
    args = {
        "prompt": f"Character1 {prompt}",
        "aspect_ratio": aspect_ratio,
        "resolution": "720p",
        "duration": duration,
        "enable_audio": False,
        "enable_prompt_expansion": True,
    }
    if video_url:
        args["video_urls"] = [video_url]
    if image_url:
        args["image_urls"] = [image_url]

    result = fal_client.subscribe("wan/v2.6/reference-to-video/flash", arguments=args)
    return result["video"]["url"]


def generate_cinematic(prompt: str, image_url: str, aspect_ratio: str = "16:9") -> str:
    """Generate cinematic multi-shot sequence via Kling 2.1 Pro. Returns video URL."""
    multi_shot_prompt = (
        f"[Shot 1: Establishing, 3s] {prompt} - Wide shot, camera slowly dollies in. "
        f"[Shot 2: Medium shot, 4s] Subject walks toward camera, confident posture. "
        f"[Shot 3: Close-up, 3s] Hands gesturing, warm lighting, soft bokeh background. "
        f"[Shot 4: Reaction shot, 3s] Subject turns to camera with slight smile."
    )

    result = fal_client.subscribe(
        "fal-ai/kling-video/v2.1/pro/image-to-video",
        arguments={
            "prompt": multi_shot_prompt,
            "image_url": image_url,
            "duration": "10",
            "aspect_ratio": aspect_ratio,
        },
    )
    return result["video"]["url"]


def generate_thumbnail(prompt: str) -> str:
    """Generate thumbnail via FLUX Schnell. Returns image URL."""
    result = fal_client.subscribe(
        "fal-ai/flux/schnell",
        arguments={
            "prompt": prompt,
            "image_size": "landscape_16_9",
            "num_images": 1,
        },
    )
    return result["images"][0]["url"]
__all__ = ['generate_broll', 'generate_cinematic', 'generate_thumbnail']
