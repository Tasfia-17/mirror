#!/usr/bin/env python3
"""Example of using MIRROR via the FastAPI endpoint."""
import requests

files = {"file": open("voice_memo.mp3", "rb")}
resp = requests.post("http://localhost:8000/generate", files=files)
job_id = resp.json()["job_id"]

import time
while True:
    status = requests.get(f"http://localhost:8000/jobs/{job_id}").json()
    if status["status"] == "complete":
        print(f"Done! {status['result']['total_outputs']} outputs")
        break
    time.sleep(3)
