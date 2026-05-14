"""Hyperframes Agent -- HTML-to-video composition with animated overlays."""
from core.state import MirrorState
from clients import posthog_client


PLATFORM_TEMPLATES = {
    "linkedin": """<div id="stage" data-composition-id="linkedin-video" data-start="0" data-width="1080" data-height="1080">
  <video id="avatar" data-start="0" data-duration="45" data-track-index="0" src="{video_url}" />
  <div class="lower-third" data-start="2" data-duration="5" data-track-index="1"
       style="position:absolute;bottom:100px;left:50px;background:rgba(0,0,0,0.8);padding:20px;color:white;">
    <h2 style="font-size:32px;margin:0;">{hook}</h2>
  </div>
  <div class="cta" data-start="40" data-duration="5" data-track-index="2"
       style="position:absolute;bottom:50px;right:50px;background:#0077b5;padding:15px 30px;color:white;border-radius:8px;">
    <p style="font-size:24px;margin:0;">Connect on LinkedIn</p>
  </div>
</div>""",

    "tiktok": """<div id="stage" data-composition-id="tiktok-video" data-start="0" data-width="1080" data-height="1920">
  <video id="avatar" data-start="0" data-duration="30" data-track-index="0" src="{video_url}" />
  <div class="flash-hook" data-start="0" data-duration="1" data-track-index="1"
       style="position:absolute;top:100px;left:0;right:0;text-align:center;font-size:48px;color:white;text-shadow:2px 2px 4px black;">
    <h1>{hook}</h1>
  </div>
  <div class="cta" data-start="25" data-duration="5" data-track-index="2"
       style="position:absolute;bottom:150px;left:0;right:0;text-align:center;">
    <p style="font-size:36px;color:white;text-shadow:2px 2px 4px black;">Follow for more</p>
  </div>
</div>""",

    "youtube": """<div id="stage" data-composition-id="youtube-video" data-start="0" data-width="1920" data-height="1080">
  <video id="avatar" data-start="0" data-duration="60" data-track-index="0" src="{video_url}" />
  <div class="lower-third" data-start="3" data-duration="6" data-track-index="1"
       style="position:absolute;bottom:80px;left:60px;border-left:6px solid #ff0000;padding-left:16px;color:white;">
    <h2 style="font-size:28px;margin:0;">{hook}</h2>
  </div>
  <div class="subscribe" data-start="55" data-duration="5" data-track-index="2"
       style="position:absolute;bottom:40px;right:60px;background:#ff0000;padding:12px 24px;color:white;border-radius:4px;">
    <p style="font-size:20px;margin:0;">Subscribe</p>
  </div>
</div>""",

    "sales": """<div id="stage" data-composition-id="sales-video" data-start="0" data-width="1920" data-height="1080">
  <video id="avatar" data-start="0" data-duration="45" data-track-index="0" src="{video_url}" />
  <div class="headline" data-start="1" data-duration="4" data-track-index="1"
       style="position:absolute;top:60px;left:0;right:0;text-align:center;color:white;font-size:36px;font-weight:bold;">
    <p>{hook}</p>
  </div>
  <div class="cta" data-start="40" data-duration="5" data-track-index="2"
       style="position:absolute;bottom:60px;left:0;right:0;text-align:center;">
    <a style="background:#00c851;padding:16px 40px;color:white;font-size:24px;border-radius:6px;">Book a Call</a>
  </div>
</div>""",

    "podcast": """<div id="stage" data-composition-id="podcast-video" data-start="0" data-width="1920" data-height="1080">
  <video id="avatar" data-start="0" data-duration="60" data-track-index="0" src="{video_url}" />
  <div class="waveform" data-start="0" data-duration="60" data-track-index="1"
       style="position:absolute;bottom:40px;left:0;right:0;height:80px;background:rgba(0,0,0,0.5);">
    <canvas id="waveform-canvas" width="1920" height="80"></canvas>
  </div>
  <div class="episode-title" data-start="2" data-duration="5" data-track-index="2"
       style="position:absolute;top:40px;left:60px;color:white;font-size:24px;">
    <p>{hook}</p>
  </div>
</div>""",
}


def render_template(platform: str, video_url: str, hook: str) -> str:
    """Return Hyperframes HTML composition for a given platform."""
    template = PLATFORM_TEMPLATES.get(platform, PLATFORM_TEMPLATES["linkedin"])
    return template.format(video_url=video_url, hook=hook[:80])


def run(state: MirrorState) -> MirrorState:
    """Compose final videos with Hyperframes HTML overlays."""
    user_id = state["user_id"]
    videos = state.get("videos", {})
    scripts = state.get("scripts", {})

    if not videos:
        return state

    composed = {}
    for platform, video_url in videos.items():
        script = scripts.get(platform, "")
        # Extract hook: first sentence of script
        hook = script.split(".")[0] if script else platform.title()
        render_template(platform, video_url, hook)
        composed[platform] = f"{video_url}?composed=true&platform={platform}"

        posthog_client.capture(user_id, "hyperframes_compose", {
            "platform": platform,
            "hook_length": len(hook),
            "trace_id": state.get("trace_id"),
        })

    state["videos"] = composed
    return state
__all__ = ['run']
