# MIRROR Architecture

## Overview

MIRROR is a multi-agent pipeline built with LangGraph that transforms
a 60-second voice memo into 50 pieces of platform-optimized content.

## Agent Flow

```
Intake -> Identity -> Format -> Critic -> [Quality Gate]
                                   |           |
                                   v           v
                              if score < 7   if score >= 7
                              loop back      proceed
                                             |
                                             v
                              Cinematic -> Hyperframes -> Translate -> Optimizer
```

## Key Design Decisions

### Conditional Graph vs Sequential Pipeline

The Critic agent uses conditional edges to loop back to Format if
quality scores are below 7/10. This makes MIRROR an agent system
rather than a sequential pipeline.

### Async Parallelization

The Format agent uses asyncio.gather to run 5 LLM calls in parallel,
reducing format time from 10s to 2s.

### PostHog as the Nervous System

Every agent decision is tracked as a PostHog event. The Optimizer
agent reads quality scores and surfaces improvement signals.

## State Management

MirrorState is a TypedDict that flows through all agents. Each agent
reads from state and writes back to state. LangGraph handles the
state transitions.

## Error Handling

- Retry decorator with exponential backoff on all API calls
- Errors list in state captures non-fatal errors
- PostHog captures all errors for debugging
