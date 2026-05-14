#!/usr/bin/env python3
"""MIRROR CLI -- 60 seconds of voice into 50 pieces of content."""
import sys
import json
from pathlib import Path
from core.orchestrator import run_pipeline


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python mirror.py <audio_file.mp3> [user_id]")
        print("       python mirror.py --dry-run")
        sys.exit(1)

    if sys.argv[1] == "--dry-run":
        from dry_run import dry_run
        dry_run()
        return

    audio_path = sys.argv[1]
    user_id = sys.argv[2] if len(sys.argv) > 2 else None

    if not Path(audio_path).exists():
        print(f"Error: {audio_path} not found")
        sys.exit(1)

    print(f"MIRROR -- Processing {audio_path}")
    print("=" * 60)

    result = run_pipeline(audio_path, user_id=user_id)

    print("\nPipeline complete!")
    print(f"Duration:        {result['duration_seconds']:.1f}s")
    print(f"Transcript:      {(result['transcript'] or '')[:100]}...")
    print(f"Emotion:         {result['emotion']}")
    print(f"Videos:          {len(result['videos'])} ({', '.join(result['videos'].keys())})")
    print(f"Translations:    {len(result['translations'])} languages")
    print(f"Total outputs:   {result['total_outputs']}")
    print(f"Quality scores:  {result.get('quality_scores')}")
    print(f"User ID:         {result['user_id']}")
    print(f"Trace ID:        {result['trace_id']}")

    if result["errors"]:
        print(f"\nErrors: {result['errors']}")

    print("\nFull result:")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
