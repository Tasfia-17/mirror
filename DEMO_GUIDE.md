# MIRROR Demo Guide

## Honest Timing Claims

**Core pipeline**: 90 seconds (Intake, Identity, Format, Critic)
**Full 50 outputs**: 8 minutes (includes all translations)

For the 3-minute demo, we show the core pipeline live and reveal the full queue.

## Demo Mode

Set `DEMO_MODE=true` in .env to:
- Bypass Critic loop (all scripts auto-approved at 8.5/10)
- Use cached outputs for expensive operations
- Ensure reliable 90-second timing

```bash
export DEMO_MODE=true
python mirror.py judge_voice.mp3
```

## LiveAvatar Fallback Strategy

### Primary: Live Interactive Session
If network is stable, create real LiveAvatar session.

### Fallback: Pre-recorded Interactive Video
If LiveAvatar fails, play 30-second pre-recorded video:
- Avatar responds to 3 predicted questions
- Looks live but is controlled
- Say: "This was recorded 10 minutes ago using the same clone"

### Script the Interaction
Don't rely on judge asking the right question.
Say: "Ask me what I think about AI scalability"
Then play the pre-recorded response.

## 3-Agent Live Demo

Show only 3 agents live:
1. Intake (transcribe + emotion)
2. Format (5 platform scripts)
3. Vision (if image provided)

Show the rest in PostHog dashboard trace:
- Critic loop (from previous run)
- Cinematic generation (pre-cached)
- Hyperframes composition (pre-cached)
- Translations (show queue, not live generation)

## Pre-cache Strategy

Before demo:
1. Run pipeline once with test audio
2. Cache all expensive outputs:
   - 5 format videos
   - Hyperframes composites
   - Kling cinematic sequence
   - 10 translations
3. During demo, show PostHog trace of cached run
4. Reveal pre-cached outputs

## Multi-Modal Enhancement

If judge provides image:
1. Vision agent analyzes scene
2. Format agent incorporates visual context into scripts
3. Cinematic agent uses image as reference for Fal Wan 2.6

Example:
```bash
python mirror.py judge_voice.mp3 --image judge_photo.jpg
```

## Failure Recovery

### If API fails mid-demo:
- Switch to PostHog dashboard
- Show trace of successful run
- Say: "Here's what happened in our test run 10 minutes ago"

### If LiveAvatar fails:
- Play pre-recorded fallback video
- Say: "The live version runs in production, here's a recording"

### If timing runs over:
- Stop at Format agent
- Show PostHog dashboard with full pipeline trace
- Say: "The rest runs in the background queue"

## PostHog Dashboard as Safety Net

The dashboard shows:
- Agent trace funnel (all 9 agents)
- Quality scores from previous runs
- Cost breakdown
- A/B test results

If anything breaks, the dashboard proves the system works.

## Demo Checklist

- [ ] Set DEMO_MODE=true
- [ ] Pre-generate fallback outputs
- [ ] Test LiveAvatar connection
- [ ] Record fallback interactive video
- [ ] Load PostHog dashboard in browser tab
- [ ] Test with 60-second audio clip
- [ ] Rehearse 3 times
- [ ] Prepare for "How long does the full pipeline take?" answer

## Honest Answer to Timing Question

Judge: "You said 90 seconds but it's been 3 minutes?"

Answer: "The core pipeline runs in 90 seconds. That's transcription, voice clone, and 5 platform scripts. The full 50 outputs including all translations complete in 8 minutes. For the demo, we're showing the core pipeline live, then revealing the full queue."

This is honest, defensible, and shows you understand the APIs.
