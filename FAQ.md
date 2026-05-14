# Frequently Asked Questions

## General

**Q: How much does it cost per generation?**
A: Approximately $4.20 for 60s input generating 50 outputs (5 formats x 10 languages).

**Q: How long does it take?**
A: 15-90 seconds depending on API latency. Most generations complete in under 30s.

**Q: Can I use my own avatar?**
A: Yes. Upload a 15-second video of yourself to HeyGen and use the avatar_id in the Identity agent.

## Technical

**Q: Why does the Critic loop back to Format?**
A: If any script scores below 7/10, the system rewrites it (max 2 attempts) before expensive video generation.

**Q: Can I add more languages?**
A: Yes. Edit LANGUAGES in config.py. HeyGen supports 40+ languages.

**Q: Can I customize the format guidelines?**
A: Yes. Edit FORMAT_GUIDELINES in core/prompts.py or use PostHog feature flags for runtime updates.

## Troubleshooting

**Q: Why is my generation failing?**
A: Check your API keys and credits. Run python dry_run.py to estimate costs first.

**Q: Can I run this without PostHog?**
A: Yes, but you will lose observability. Set POSTHOG_API_KEY to a dummy value.
