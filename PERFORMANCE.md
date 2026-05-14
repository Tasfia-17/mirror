# Performance Optimization

## Async Parallelization

The Format agent uses asyncio.gather to run 5 LLM calls in parallel.
This reduces format time from 10s to 2s.

## Caching

Consider caching voice clones and avatars for repeat users.
ElevenLabs IVC and HeyGen Avatar V are one-time costs.

## Batch Processing

Process multiple voice memos in parallel using multiprocessing:

```python
from multiprocessing import Pool
from core.orchestrator import run_pipeline

audio_files = ["file1.mp3", "file2.mp3", "file3.mp3"]
with Pool(3) as p:
    results = p.map(run_pipeline, audio_files)
```

## API Rate Limits

HeyGen: 10 concurrent jobs on pay-as-you-go
ElevenLabs: Depends on your plan
Fal: No documented limits

Use exponential backoff (already implemented in core/retry.py).
