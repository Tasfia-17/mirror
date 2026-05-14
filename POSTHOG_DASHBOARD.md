# PostHog Dashboard Configuration

## Dashboard 1: Agent Trace Funnel

**Name**: MIRROR Agent Pipeline  
**Type**: Funnel

**Steps**:
1. `mirror_pipeline_start` → Intake
2. `mirror_pipeline_step` (step=intake_transcribe) → Identity
3. `mirror_pipeline_step` (step=identity_voice_clone) → Format
4. `mirror_pipeline_step` (step=format_rewrite_*) → Critic
5. `critic_evaluation` → Output
6. `mirror_pipeline_complete` → Done

**Metrics**:
- Conversion rate at each step
- Average duration per step (from `duration_ms` property)
- Drop-off points

**Filters**:
- Group by `trace_id` to see individual runs
- Filter by `user_id` for specific users

---

## Dashboard 2: Quality Scores

**Name**: Critic Agent Scores  
**Type**: Bar Chart

**Event**: `critic_evaluation`  
**Y-axis**: Average of `score` property  
**X-axis**: `platform` property (LinkedIn, TikTok, YouTube, Sales, Podcast)

**Breakdown**: 
- `hook_score`
- `cta_score`
- `emotion_score`
- `platform_score`

**Goal Line**: 7.0 (minimum passing score)

---

## Dashboard 3: Generation Cost

**Name**: Cost Breakdown  
**Type**: Pie Chart

**Event**: `generation_cost`  
**Segments**:
- `elevenlabs_cost`
- `heygen_cost`
- `fal_cost`
- `openai_cost`

**Total**: Sum of `total_cost` property

**Additional Metrics**:
- Average cost per generation
- Margin calculation: `$199 - total_cost` (Pro tier)
- Cost per output minute

---

## Feature Flag: Prompt A/B Test

**Flag Name**: `prompt_linkedin_hook`

**Variants**:
- **Control (50%)**: "Start with a question that challenges conventional wisdom"
- **Test (50%)**: "Open with a bold statement that triggers curiosity"

**Metric**: `critic_evaluation.score` where `platform=linkedin`

**Rollout**: 100% of users

---

## Prompt Management

**Prompt ID**: `format_linkedin`

**Version 1** (Current):
```
Rewrite this transcript for LinkedIn format.
Professional, value-driven. Start with insight. End with question to drive comments. 30-45 sec.
```

**Version 2** (Test):
```
Rewrite this transcript for LinkedIn format.
Hook: Challenge conventional wisdom in first 3 seconds.
Body: Share one counterintuitive insight with proof.
CTA: Ask a question that sparks debate. 30-45 sec.
```

**Fetch at runtime**:
```python
from clients.posthog_client import fetch_prompt
prompt = fetch_prompt("format_linkedin", user_id, default=DEFAULT_PROMPT)
```

---

## Setup Instructions

1. **Create PostHog Project**: https://app.posthog.com
2. **Add API Key** to `.env`: `POSTHOG_API_KEY=phc_...`
3. **Create Dashboards**: Copy configurations above
4. **Create Feature Flag**: `prompt_linkedin_hook` with 2 variants
5. **Add Prompt**: In PostHog UI → Prompts → New Prompt → `format_linkedin`
6. **Run Pipeline**: Events will populate automatically

---

## Live Demo Flow

1. **Before generation**: Show empty dashboard
2. **During generation**: Refresh to show events flowing in real-time
3. **After generation**: 
   - Show funnel: All steps completed
   - Show quality scores: Bar chart with scores
   - Show cost breakdown: Pie chart
4. **A/B Test**: Click into feature flag, show 50/50 split
5. **Prompt Update**: Edit prompt in PostHog UI, trigger new generation, show it using new prompt

---

## Mock Data (For Demo Prep)

If you need to pre-populate the dashboard:

```python
# scripts/populate_posthog.py
import posthog
from config import POSTHOG_API_KEY

posthog.project_api_key = POSTHOG_API_KEY
posthog.host = "https://app.posthog.com"

# Generate 10 sample traces
for i in range(10):
    trace_id = f"demo_trace_{i}"
    user_id = f"demo_user_{i}"
    
    posthog.capture(user_id, "mirror_pipeline_start", {"trace_id": trace_id})
    posthog.capture(user_id, "mirror_pipeline_step", {"trace_id": trace_id, "step": "intake_transcribe", "duration_ms": 3200})
    posthog.capture(user_id, "critic_evaluation", {"trace_id": trace_id, "platform": "linkedin", "score": 8.5, "hook_score": 9, "cta_score": 8})
    posthog.capture(user_id, "generation_cost", {"trace_id": trace_id, "elevenlabs_cost": 0.20, "heygen_cost": 3.00, "fal_cost": 1.00, "total_cost": 4.20})
    posthog.capture(user_id, "mirror_pipeline_complete", {"trace_id": trace_id, "duration_seconds": 18.5})

posthog.flush()
```
