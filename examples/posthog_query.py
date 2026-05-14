"""Example of querying PostHog for analytics."""
from clients.posthog_client import posthog

# Query average quality scores
events = posthog.get_events(
    event="critic_evaluation",
    properties={"platform": "linkedin"}
)
scores = [e["properties"]["score"] for e in events]
avg = sum(scores) / len(scores) if scores else 0
print(f"Average LinkedIn score: {avg:.2f}")
