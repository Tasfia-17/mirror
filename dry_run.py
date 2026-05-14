#!/usr/bin/env python3
"""MIRROR -- dry-run cost estimation before running the pipeline."""
import sys
from core.cost import calculate_generation_cost, PRICING


def dry_run(input_sec: int = 60, output_sec: int = 30,
            formats: int = 5, languages: int = 10):
    """Print cost estimate without calling any APIs."""
    cost = calculate_generation_cost(input_sec, output_sec, formats, languages)

    print("MIRROR -- Cost Estimate (dry run)")
    print("=" * 50)
    print(f"Input:   {input_sec}s voice memo")
    print(f"Output:  {output_sec}s per video, {formats} formats, {languages} languages")
    print(f"Total outputs: {cost['total_outputs']}")
    print()
    print("Cost breakdown:")
    print(f"  ElevenLabs Scribe v2:     ${cost['elevenlabs_transcribe']:.4f}")
    print(f"  ElevenLabs IVC:           ${cost['elevenlabs_ivc']:.4f}")
    print(f"  OpenAI GPT-4o-mini:       ${cost['openai_llm']:.4f}")
    print(f"  HeyGen Video Agent:       ${cost['heygen_videos']:.4f}")
    print(f"  Fal Kling B-roll:         ${cost['fal_broll']:.4f}")
    print(f"  Fal FLUX thumbnails:      ${cost['fal_thumbnails']:.4f}")
    print(f"  HeyGen Video Translate:   ${cost['heygen_translations']:.4f}")
    print(f"  {'':40} --------")
    print(f"  Total:                    ${cost['total']:.2f}")
    print(f"  Per output:               ${cost['cost_per_output']:.4f}")
    print()
    print("Pricing tiers:")
    for tier, pricing in PRICING.items():
        print(f"  {tier.capitalize()}: ${pricing['price_monthly']}/mo "
              f"({pricing['minutes_included']} min included)")


if __name__ == "__main__":
    dry_run()
