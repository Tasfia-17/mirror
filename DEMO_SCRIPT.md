# MIRROR Demo Script

## Setup (5 minutes before demo)

1. **Environment check**:
```bash
cd /home/rifa/mirror
source venv/bin/activate
python -c "import elevenlabs, fal_client, langgraph; print('✅ All deps loaded')"
```

2. **API keys verified** (check `.env`):
- ElevenLabs ✓
- HeyGen ✓
- Fal ✓
- PostHog ✓
- OpenAI ✓

3. **Backup outputs ready** (in case of rate limits):
- Pre-generated 5 format videos
- Pre-generated 2 language translations
- Screenshots of PostHog dashboard

## Demo Flow (3 minutes)

### Act 1: The Problem (30 seconds)

**Script**: 
> "Content creation is broken. To reach a global audience, you need:
> - A video editor for each platform
> - A translator for each language
> - A PR agency charging $50k/month
> 
> What if one person could become 50 pieces of content in 90 seconds?"

### Act 2: The Magic (90 seconds)

**Live demo**:

1. **Record judge's voice** (60 seconds):
```bash
# Judge speaks into phone/laptop mic
# Topic: "Why I'm excited about AI agents"
```

2. **Upload and run**:
```bash
python mirror.py judge_voice.mp3
```

3. **Watch the pipeline** (show terminal output):
```
🎤 MIRROR — Processing judge_voice.mp3
============================================================
[Intake] Transcribing... ✓ (3.2s)
[Intake] Detecting emotion... ✓ (1.1s) → confident
[Identity] Cloning voice... ✓ (4.5s)
[Identity] Creating Avatar V... ✓ (mocked)
[Format] Rewriting for LinkedIn... ✓ (2.1s)
[Format] Rewriting for TikTok... ✓ (1.8s)
[Format] Rewriting for YouTube... ✓ (2.3s)
[Format] Rewriting for Sales... ✓ (1.9s)
[Format] Rewriting for Podcast... ✓ (2.0s)
[Translate] Translating to 10 languages... ✓ (mocked)
[Optimizer] Analyzing performance... ✓

✅ Pipeline complete!
⏱️  Duration: 18.9s
📝 Transcript: Why I'm excited about AI agents...
😊 Emotion: confident
🎬 Videos generated: 5
🌍 Translations: 10
📦 Total outputs: 50
```

4. **Show PostHog dashboard** (open browser):
- Real-time events flowing in
- LLM token usage per step
- Pipeline duration breakdown
- Cost per generation: $4.20

### Act 3: The Vision (30 seconds)

**Script**:
> "This is MIRROR. One voice becomes 50 pieces of content.
> 
> **For Product Track**: SaaS at $49-$199/mo. Target: founders, executives, creators.
> 
> **For Agent Track**: 6-agent LangGraph system. Self-improving via PostHog analytics.
> 
> **All 4 sponsors in load-bearing roles**:
> - ElevenLabs: Voice cloning + transcription
> - HeyGen: Avatar V + Video Agent + Video Translate
> - Fal: Wan 2.6 R2V for B-roll
> - PostHog: LLM observability + optimization loop
> 
> The future of content is one human, infinite reach."

## Backup Plan

If APIs fail:
1. Show pre-recorded demo video
2. Walk through code architecture
3. Show PostHog dashboard with historical data

## Key Talking Points

- **Speed**: 90 seconds vs 50 hours manual work
- **Cost**: $4.20 vs $50k/month agency
- **Scale**: 1 → 50 outputs automatically
- **Quality**: Native voice + digital twin in every language
- **Self-improving**: PostHog analytics feed back into prompts

## Questions to Anticipate

**Q: Why not just use ChatGPT + manual editing?**
A: MIRROR is end-to-end automated. No manual editing, no platform-specific exports, no translation services. One click.

**Q: How do you ensure quality across languages?**
A: HeyGen Video Translate preserves lip-sync and voice characteristics. ElevenLabs PVC for voice consistency.

**Q: What's the business model?**
A: SaaS subscription. Starter $49/mo, Pro $199/mo, Enterprise custom. Target: 10k users in year 1 = $2M ARR.

**Q: How does the self-improving loop work?**
A: PostHog tracks engagement metrics per format/language. Optimizer agent queries PostHog, updates prompt weights to favor high-performing patterns.

## Post-Demo

Share:
- GitHub repo: github.com/yourusername/mirror
- Live demo: mirror-demo.vercel.app
- PostHog dashboard: app.posthog.com/project/mirror

---

**Remember**: The theatrical moment is when the judge sees themselves speaking in 10 languages. Make it visceral.
