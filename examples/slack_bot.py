#!/usr/bin/env python3
"""Example Slack bot that processes voice memos."""
from slack_bolt import App
from core.orchestrator import run_pipeline

app = App(token="xoxb-...")

@app.event("file_shared")
def handle_file(event, say):
    file_id = event["file_id"]
    # Download file, run pipeline, post results
    result = run_pipeline(f"/tmp/{file_id}.mp3")
    say(f"Generated {result['total_outputs']} outputs!")

app.start(port=3000)
