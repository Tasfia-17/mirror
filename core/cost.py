"""Cost calculator for MIRROR pricing model."""

# API costs per unit (USD)
COSTS = {
    "elevenlabs_transcribe": 0.10,    # per minute of input audio
    "elevenlabs_ivc": 0.10,           # one-time per voice clone
    "elevenlabs_tts": 0.30,           # per 1000 characters
    "heygen_video_agent": 0.0333,     # per second of output video
    "heygen_translate": 0.0333,       # per second per language (speed mode)
    "heygen_translate_precision": 0.0667,  # per second per language (precision mode)
    "fal_kling": 0.10,                # per second of output video
    "fal_wan": 0.15,                  # per 5-second clip
    "fal_flux": 0.05,                 # per image
    "openai_gpt4o_mini_input": 0.15 / 1_000_000,   # per input token
    "openai_gpt4o_mini_output": 0.60 / 1_000_000,  # per output token
}

# Pricing tiers
PRICING = {
    "starter": {
        "price_monthly": 49,
        "minutes_included": 20,
        "overage_per_min": 3.00,
    },
    "pro": {
        "price_monthly": 199,
        "minutes_included": 120,
        "overage_per_min": 2.00,
    },
    "enterprise": {
        "price_monthly": 499,
        "minutes_included": 500,
        "overage_per_min": 1.50,
    },
}


def calculate_generation_cost(
    input_duration_sec: int = 60,
    output_duration_sec: int = 30,
    num_formats: int = 5,
    num_languages: int = 10,
) -> dict:
    """Calculate cost for one MIRROR generation.

    Args:
        input_duration_sec: Length of the input voice memo in seconds.
        output_duration_sec: Target length of each output video in seconds.
        num_formats: Number of platform formats to generate.
        num_languages: Number of translation languages.

    Returns:
        Dict with per-service cost breakdown and total.
    """
    input_min = input_duration_sec / 60

    transcribe = COSTS["elevenlabs_transcribe"] * input_min
    voice_clone = COSTS["elevenlabs_ivc"]

    # LLM calls: emotion detection + 5 format rewrites + 5 critic evaluations
    llm_input_tokens = 800 * (1 + num_formats * 2)
    llm_output_tokens = 300 * (1 + num_formats * 2)
    llm = (
        llm_input_tokens * COSTS["openai_gpt4o_mini_input"]
        + llm_output_tokens * COSTS["openai_gpt4o_mini_output"]
    )

    videos = COSTS["heygen_video_agent"] * output_duration_sec * num_formats
    broll = COSTS["fal_kling"] * 10 * num_formats  # 10s clip per format
    thumbnails = COSTS["fal_flux"] * num_formats
    translations = COSTS["heygen_translate"] * output_duration_sec * num_languages

    total = transcribe + voice_clone + llm + videos + broll + thumbnails + translations

    return {
        "elevenlabs_transcribe": round(transcribe, 4),
        "elevenlabs_ivc": round(voice_clone, 4),
        "openai_llm": round(llm, 4),
        "heygen_videos": round(videos, 4),
        "fal_broll": round(broll, 4),
        "fal_thumbnails": round(thumbnails, 4),
        "heygen_translations": round(translations, 4),
        "total": round(total, 2),
        "formats": num_formats,
        "languages": num_languages,
        "total_outputs": num_formats + num_formats * num_languages,
        "cost_per_output": round(total / (num_formats + num_formats * num_languages), 4),
    }


def calculate_margin(tier: str, generations_used: int) -> dict:
    """Calculate margin for a given tier and number of generations used.

    Args:
        tier: Pricing tier (starter/pro/enterprise).
        generations_used: Number of full pipeline runs (each = 1 voice memo in).
    """
    pricing = PRICING[tier]
    revenue = pricing["price_monthly"]

    cost_per_gen = calculate_generation_cost(60, 30)["total"]
    total_cost = cost_per_gen * generations_used

    if generations_used > pricing["minutes_included"]:
        overage = generations_used - pricing["minutes_included"]
        revenue += overage * pricing["overage_per_min"]

    margin = revenue - total_cost
    margin_pct = (margin / revenue * 100) if revenue > 0 else 0

    return {
        "tier": tier,
        "revenue": round(revenue, 2),
        "cost": round(total_cost, 2),
        "margin": round(margin, 2),
        "margin_pct": round(margin_pct, 1),
        "generations_used": generations_used,
    }


if __name__ == "__main__":
    print("=== Cost per Generation ===")
    cost = calculate_generation_cost()
    for k, v in cost.items():
        print(f"  {k}: {v}")

    print("\n=== Margin Analysis ===")
    for tier in ["starter", "pro", "enterprise"]:
        minutes = int(PRICING[tier]["minutes_included"] * 0.8)
        m = calculate_margin(tier, minutes)
        print(f"\n{tier.upper()} (80% utilization):")
        print(f"  Revenue: ${m['revenue']}")
        print(f"  Cost:    ${m['cost']}")
        print(f"  Margin:  ${m['margin']} ({m['margin_pct']}%)")
