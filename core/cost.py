"""Cost calculator for MIRROR pricing model."""

# API Costs (per unit)
COSTS = {
    "elevenlabs_transcribe": 0.10,  # per minute
    "elevenlabs_ivc": 0.10,  # one-time per voice
    "elevenlabs_tts": 0.30,  # per 1000 chars
    "heygen_video": 0.30,  # per minute
    "heygen_translate": 0.15,  # per minute per language
    "fal_kling": 0.25,  # per 10 seconds
    "fal_wan": 0.15,  # per 5 seconds
    "openai_gpt4o_mini": 0.15 / 1_000_000,  # per input token
}


def calculate_generation_cost(duration_seconds: int, num_formats: int = 5, num_languages: int = 10) -> dict:
    """Calculate cost for one generation based on output duration."""
    
    duration_min = duration_seconds / 60
    
    # One-time costs
    transcribe = COSTS["elevenlabs_transcribe"] * 1  # 60s input
    voice_clone = COSTS["elevenlabs_ivc"]
    
    # Per-format costs
    script_rewrites = COSTS["openai_gpt4o_mini"] * 500 * num_formats  # ~500 tokens per rewrite
    videos = COSTS["heygen_video"] * duration_min * num_formats
    
    # Cinematic (optional, 1 per format)
    broll = COSTS["fal_kling"] * (10 / 10) * num_formats  # 10s clips
    
    # Translation (per format × languages)
    translations = COSTS["heygen_translate"] * duration_min * num_formats * num_languages
    
    total = transcribe + voice_clone + script_rewrites + videos + broll + translations
    
    return {
        "transcribe": round(transcribe, 2),
        "voice_clone": round(voice_clone, 2),
        "script_rewrites": round(script_rewrites, 2),
        "videos": round(videos, 2),
        "broll": round(broll, 2),
        "translations": round(translations, 2),
        "total": round(total, 2),
        "per_output_minute": round(total / (duration_min * num_formats * (1 + num_languages)), 2)
    }


# Pricing Tiers (per-minute model)
PRICING = {
    "starter": {
        "price_monthly": 49,
        "minutes_included": 20,  # 20 minutes of final video
        "overage_per_min": 3.00,
    },
    "pro": {
        "price_monthly": 199,
        "minutes_included": 120,  # 120 minutes of final video
        "overage_per_min": 2.00,
    },
    "enterprise": {
        "price_monthly": 499,
        "minutes_included": 500,
        "overage_per_min": 1.50,
    }
}


def calculate_margin(tier: str, minutes_used: int) -> dict:
    """Calculate margin for a given tier and usage."""
    
    pricing = PRICING[tier]
    revenue = pricing["price_monthly"]
    
    # Cost calculation (assuming 30s average output)
    cost_per_min = calculate_generation_cost(30)["per_output_minute"]
    total_cost = cost_per_min * minutes_used
    
    # Overage revenue
    if minutes_used > pricing["minutes_included"]:
        overage_mins = minutes_used - pricing["minutes_included"]
        revenue += overage_mins * pricing["overage_per_min"]
    
    margin = revenue - total_cost
    margin_pct = (margin / revenue * 100) if revenue > 0 else 0
    
    return {
        "tier": tier,
        "revenue": round(revenue, 2),
        "cost": round(total_cost, 2),
        "margin": round(margin, 2),
        "margin_pct": round(margin_pct, 1),
        "minutes_used": minutes_used,
        "breakeven_minutes": round(revenue / cost_per_min, 1)
    }


# Example calculations
if __name__ == "__main__":
    print("=== Cost per Generation ===")
    for duration in [15, 30, 60, 300]:
        cost = calculate_generation_cost(duration)
        print(f"\n{duration}s output:")
        print(f"  Total: ${cost['total']}")
        print(f"  Per output minute: ${cost['per_output_minute']}")
    
    print("\n=== Margin Analysis ===")
    for tier in ["starter", "pro", "enterprise"]:
        # Assume 80% utilization
        minutes = int(PRICING[tier]["minutes_included"] * 0.8)
        margin = calculate_margin(tier, minutes)
        print(f"\n{tier.upper()} (80% utilization):")
        print(f"  Revenue: ${margin['revenue']}")
        print(f"  Cost: ${margin['cost']}")
        print(f"  Margin: ${margin['margin']} ({margin['margin_pct']}%)")
        print(f"  Breakeven: {margin['breakeven_minutes']} min/mo")
