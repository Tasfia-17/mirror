#!/usr/bin/env python3
"""Basic MIRROR usage example."""
from core.orchestrator import run_pipeline

result = run_pipeline("voice_memo.mp3", user_id="demo_user")
print(f"Generated {result['total_outputs']} outputs in {result['duration_seconds']:.1f}s")
print(f"Quality scores: {result['quality_scores']}")
