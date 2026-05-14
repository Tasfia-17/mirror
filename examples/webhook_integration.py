#!/usr/bin/env python3
"""Example of triggering MIRROR from a webhook."""
from fastapi import FastAPI, BackgroundTasks
from core.orchestrator import run_pipeline

app = FastAPI()

@app.post("/webhook/voice-memo")
async def handle_voice_memo(url: str, background_tasks: BackgroundTasks):
    """Download audio from URL and process."""
    import requests
    audio = requests.get(url).content
    with open("/tmp/voice.mp3", "wb") as f:
        f.write(audio)
    background_tasks.add_task(run_pipeline, "/tmp/voice.mp3")
    return {"status": "processing"}
