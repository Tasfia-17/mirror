#!/usr/bin/env python3
"""MIRROR CLI -- 60 seconds of voice into 50 pieces of content."""
import sys
import json
from pathlib import Path
from core.orchestrator import run_pipeline


def main():
    if len(sys.argv) < 2:
        print("Usage: python mirror.py <audio_file.mp3>")
        sys.exit(1)

    audio_path = sys.argv[1]

    if not Path(audio_path).exists():
        print(f"Error: {audio_path} not found")
        sys.exit(1)

    print(f"MIRROR -- Processing {audio_path}")
    print("=" * 60)

    result = run_pipeline(audio_path)

    print("\nPipeline complete!")
    print(f"Duration: {result['duration_seconds']:.1f}s")
    print(f"Transcript: {(result['transcript'] or '')[:100]}...")
    print(f"Emotion: {result['emotion']}")
    print(f"Videos generated: {len(result['videos'])}")
    print(f"Translations: {len(result['translations'])}")
    print(f"Total outputs: {result['total_outputs']}")
    print(f"Quality scores: {result.get('quality_scores')}")
    print(f"User ID: {result['user_id']}")
    print(f"Trace ID: {result['trace_id']}")

    if result["errors"]:
        print(f"\nErrors: {result['errors']}")

    print("\nFull result:")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
