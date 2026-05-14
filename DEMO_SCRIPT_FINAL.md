# MIRROR — 3-Minute Demo Script (FINAL)

**Total Time**: 3:00  
**Judges**: HeyGen, ElevenLabs, Fal, PostHog teams + VCs

---

## PROBLEM (20 seconds)

> "Content creation is culturally broken.
> 
> To reach a global audience, you need a video editor for each platform, a translator for each language, and a PR agency charging $50,000 a month.
> 
> What if one person could become 50 pieces of culturally-aware content in 90 seconds?"

**[Pause for effect]**

---

## MAGIC (90 seconds)

### Setup (10s)

> "Let me show you. [Judge's name], can you speak for 60 seconds on any topic? Your choice."

**[Judge speaks into mic — record audio]**

### The Generation (60s)

**[Upload audio, hit Enter]**

**[Screen shows terminal output with live progress]:**

```
🎤 MIRROR — Processing judge_voice.mp3
============================================================
[Intake] ✓ Transcribed (3.2s)
[Intake] ✓ Emotion: confident
[Identity] ✓ Voice cloned (4.5s)
[Identity] ✓ Avatar created
[Format] ✓ LinkedIn script (2.1s)
[Format] ✓ TikTok script (1.8s)
[Format] ✓ YouTube script (2.3s)
[Format] ✓ Sales script (1.9s)
[Format] ✓ Podcast script (2.0s)
[Critic] ⚠️ LinkedIn score: 6.2/10 - Rewriting...
[Format] ✓ LinkedIn improved to 8.5/10
[Critic] ✓ All scripts approved
[Cinematic] ✓ 4-shot narrative generated
[Hyperframes] ✓ Composed with overlays
[Translate] ✓ 10 languages

✅ Pipeline complete!
⏱️  Duration: 18.9s
📦 Total outputs: 50
```

### The Reveal (20s)

> "In 19 seconds, we generated 50 pieces of content. But here's what makes this different..."

**[Show side-by-side]:**
- Left: Raw HeyGen video (plain avatar)
- Right: Hyperframes-composited (animated lower thirds, CTAs)

> "This isn't just a video. It's a webpage that compiles to MP4. We can A/B test the CSS."

---

## CLIMAX (30 seconds)

### The Gasp Moment

> "But we didn't just clone your voice. We cloned your presence."

**[Open browser → LiveAvatar session]**

**[Judge's avatar appears on screen, real-time]**

> "[Judge's name], ask yourself anything."

**[Judge asks]: "What did I say about AI?"**

**[Avatar responds in real-time with judge's voice]:**
> "You said AI should augment human creativity, not replace it. I can say that in Japanese if you'd like."

**[Avatar switches to Japanese, maintaining judge's face and voice tone]**

**[Audience gasps]**

---

## PROOF (30 seconds)

### The Nervous System

> "This is the nervous system."

**[Flip to PostHog dashboard — 3 panels visible]:**

1. **Agent Trace Funnel**: Shows Intake → Identity → Format → Critic → Output
2. **Quality Scores**: Bar chart showing 5 platform scores (all > 7.0)
3. **Cost Breakdown**: Pie chart — HeyGen $3.00, Fal $1.00, ElevenLabs $0.20

> "Every agent decision is tracked. The Critic scored our first LinkedIn script 6.2 out of 10, so the system rewrote it. Final score: 8.5."

**[Click into Feature Flag]:**

> "We're A/B testing two prompt versions right now. Version B is winning with 8.7 average score vs 6.2."

---

## VISION (10 seconds)

> "MIRROR doesn't translate content. It translates culture.
> 
> One human. Infinite cultures. Zero latency.
> 
> $199 a month. 89% margin. Self-improving via PostHog."

**[End]**

---

## JUDGE Q&A (Prepared Answers)

### Q: "What's your margin?"

**A**: "At Pro tier, $199 revenue minus $21 API cost equals $178 margin per customer at 80% utilization. That's 89.4%. We break even at 23 customers."

**[Show slide with cost calculator output]**

---

### Q: "How is this different from HeyGen's native product?"

**A**: "HeyGen makes videos. MIRROR makes culturally-aware, self-improving video systems with agent orchestration.

Three differences:
1. **Conditional graph** — Our Critic agent loops back if quality < 7/10. HeyGen generates once.
2. **Cultural adaptation** — We don't just translate words. We adapt hooks, pacing, and visual style for each culture.
3. **Self-improvement** — PostHog tracks which formats perform best and updates prompts at runtime. No code deploy needed."

---

### Q: "What if an agent fails?"

**A**: "Three layers of resilience:

1. **Critic Agent** — Catches weak outputs before expensive video generation
2. **Retry logic** — Exponential backoff on all API calls (3 attempts max)
3. **PostHog alerts** — If error rate > 5%, we get notified and the Optimizer agent adjusts"

**[Show retry decorator in code if they want proof]**

---

### Q: "Can you show me the code?"

**A**: "Absolutely. Here's the conditional edge in our LangGraph orchestrator."

**[Open `core/orchestrator.py`, scroll to `route_by_quality` function]:**

```python
def route_by_quality(state: MirrorState) -> str:
    """Route based on critic scores. Loop back if quality < 7/10."""
    scores = state.get("quality_scores", {})
    min_score = min(scores.values())
    
    if min_score < 7.0 and state.get("rewrite_count", 0) < 2:
        return "rewrite"  # Loop back to Format agent
    return "proceed"  # Continue to Cinematic
```

> "This is what makes it an agent system, not a pipeline."

---

### Q: "What's your go-to-market?"

**A**: "Three channels:

1. **Product Hunt launch** — Target: 500 signups in week 1
2. **LinkedIn outreach** — Founders with 10k+ followers who post daily
3. **Agency partnerships** — White-label for PR agencies at $499/mo Enterprise tier

We're pre-revenue. First paying customer in 2 weeks."

---

### Q: "What's the biggest risk?"

**A**: "API rate limits during viral growth. 

Mitigation: We're building a queue system with Redis. If HeyGen hits rate limit, we queue the job and notify the user via email when it's done. Expected wait: < 5 minutes even at 1000 concurrent users."

---

## BACKUP PLAN (If LiveAvatar Fails)

If LiveAvatar API errors or latency > 2 seconds:

> "We also pre-recorded an interactive demo. Watch this."

**[Play 30-second video]:**
- Avatar appears
- Text overlay: "What did I say about AI?"
- Avatar responds: "You said AI should augment human creativity..."
- Text overlay: "Say it in Japanese"
- Avatar switches to Japanese

> "This is pre-recorded, but in production it's real-time via HeyGen LiveAvatar with sub-400ms latency using ElevenLabs Flash v2.5."

---

## TIMING BREAKDOWN

| Section | Time | Cumulative |
|---------|------|------------|
| Problem | 20s | 0:20 |
| Magic (Setup) | 10s | 0:30 |
| Magic (Generation) | 60s | 1:30 |
| Magic (Reveal) | 20s | 1:50 |
| Climax (LiveAvatar) | 30s | 2:20 |
| Proof (PostHog) | 30s | 2:50 |
| Vision | 10s | 3:00 |

**Total**: 3:00 exactly

---

## REHEARSAL CHECKLIST

- [ ] Time yourself 3 times — cut if over 3:00
- [ ] Test LiveAvatar with 3 sample questions
- [ ] Pre-load PostHog dashboard in browser tab
- [ ] Have cost calculator output ready as slide
- [ ] Test audio recording setup
- [ ] Prepare fallback video if LiveAvatar fails
- [ ] Print this script — memorize key phrases
- [ ] Breathe. You've built something incredible.

---

**Remember**: The judges are looking for:
1. ✅ Technical depth (conditional graph, multi-agent)
2. ✅ Sponsor integration (all 4 load-bearing)
3. ✅ Theatrical moment (LiveAvatar)
4. ✅ Business viability (89% margin)
5. ✅ Self-improvement (PostHog prompts)

**You have all 5. Now execute.** 🏆
