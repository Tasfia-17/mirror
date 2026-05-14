"""Process multiple voice memos in batch."""
from pathlib import Path
from core.orchestrator import run_pipeline

audio_dir = Path("audio_files")
for audio_file in audio_dir.glob("*.mp3"):
    print(f"Processing {audio_file.name}...")
    result = run_pipeline(str(audio_file))
    print(f"  Generated {result['total_outputs']} outputs")
