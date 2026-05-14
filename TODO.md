# MIRROR — Build Checklist

## Status Legend
- [ ] Not started
- [x] Done
- [~] In progress

---

## Phase 1: Foundation
- [x] Project structure created
- [x] TODO.md created
- [x] `.env.example` with all API keys
- [x] `requirements.txt` with pinned deps
- [x] `config.py` — central config loader

## Phase 2: Core Services (clients/)
- [x] `clients/elevenlabs.py` — transcribe + IVC clone + TTS
- [x] `clients/heygen.py` — Avatar V create + Video Agent + Video Translate + poll
- [x] `clients/fal.py` — Wan 2.6 R2V + Kling B-roll + FLUX thumbnail
- [x] `clients/posthog_client.py` — event capture + LLM tracing wrapper

## Phase 3: Agents (agents/)
- [x] `agents/intake.py` — transcribe audio, detect emotion, extract face frame
- [x] `agents/identity.py` — ElevenLabs IVC + HeyGen Avatar V creation
- [x] `agents/format.py` — LLM rewrites script for 5 formats, calls HeyGen Video Agent
- [x] `agents/cinematic.py` — Fal Wan R2V + Kling B-roll generation
- [x] `agents/translate.py` — HeyGen Video Translate × 10 languages
- [x] `agents/optimizer.py` — reads PostHog, updates prompt weights

## Phase 4: Orchestrator
- [x] `core/orchestrator.py` — LangGraph state machine wiring all 6 agents
- [x] `core/state.py` — shared MirrorState TypedDict
- [x] `core/prompts.py` — all LLM prompt templates

## Phase 5: API + UI
- [ ] `api/app.py` — FastAPI app with `/generate` endpoint
- [ ] `api/routes.py` — upload audio, SSE progress stream
- [ ] `static/index.html` — minimal demo UI

## Phase 6: CLI
- [x] `mirror.py` — CLI entry: `python mirror.py <audio_file.mp3>`

## Phase 7: Hyperframes Templates
- [ ] `static/templates/podcast.html` — waveform visualization
- [ ] `static/templates/youtube.html` — motion graphics lower thirds

## Phase 8: Verification
- [ ] End-to-end test with real audio input
- [ ] PostHog dashboard shows live events
- [ ] All 5 formats generate successfully
- [ ] At least 2 languages translate successfully
