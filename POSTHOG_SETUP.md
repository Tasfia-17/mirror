# MIRROR PostHog Dashboard Setup

Create these 3 dashboards in PostHog after running the pipeline once.

## Dashboard 1: Pipeline Funnel

**Funnel Chart: Agent Steps**
- Event: mirror_pipeline_step
- Breakdown by: step
- Order: intake_transcribe, identity_voice_clone, format_video_linkedin, critic_evaluation, cinematic_broll, hyperframes_compose, translate_videos

**Line Chart: Duration Over Time**
- Event: mirror_pipeline_complete
- Property: duration_seconds
- Aggregation: Average

## Dashboard 2: Quality Scores

**Bar Chart: Scores by Platform**
- Event: critic_evaluation
- Property: score
- Breakdown by: platform
- Aggregation: Average

**Number: Rewrite Rate**
- Event: critic_evaluation
- Filter: score < 7
- Count

## Dashboard 3: LLM Cost Tracker

**Number: Total Cost**
- Event: $ai_generation
- Property: $ai_total_cost_usd
- Sum

**Bar Chart: Latency by Step**
- Event: $ai_generation
- Property: $ai_latency
- Breakdown by: step

## Feature Flag: A/B Test

Name: prompt_linkedin_hook
Type: String
Variants: control (50%), test (50%)
