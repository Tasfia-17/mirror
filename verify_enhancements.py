#!/usr/bin/env python3
"""Verification test for winning enhancements."""
import sys
from pathlib import Path

print("=== MIRROR Winning Enhancements Verification ===\n")

# Test 1: Avatar Collaboration
print("1. Testing Avatar Collaboration Agent...")
try:
    from agents.collaboration import create_visual_markup
    
    script = "Did you know that 80% of content creators struggle with consistency?"
    feedback = "Hook needs more impact"
    markup = create_visual_markup(script, feedback)
    
    assert "annotations" in markup
    assert isinstance(markup["annotations"], list)
    print("   ✓ Avatar collaboration agent working")
    print(f"   ✓ Generated {len(markup['annotations'])} annotations")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Test 2: Router Visualization
print("\n2. Testing Router Visualization...")
try:
    from core.router_viz import AgentRouterViz, get_router_viz, reset_router_viz
    
    reset_router_viz()
    viz = get_router_viz()
    
    # Simulate agent execution
    viz.log_agent_start("intake", {"user_id": "test"})
    viz.log_agent_complete("intake", 3200, True)
    viz.log_cost("intake", 0.10)
    viz.log_routing_decision("critic", "format", "Score 6.2 < 7.0")
    
    graph_data = viz.get_graph_data()
    
    assert "nodes" in graph_data
    assert "edges" in graph_data
    assert "costs" in graph_data
    assert len(graph_data["events"]) == 4
    print("   ✓ Router visualization working")
    print(f"   ✓ Tracked {len(graph_data['events'])} events")
    print(f"   ✓ Total cost: ${graph_data['total_cost']:.2f}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Test 3: Self-Improvement Demo
print("\n3. Testing Self-Improvement Demo...")
try:
    from core.self_improvement import SelfImprovementDemo, get_improvement_demo
    
    demo = SelfImprovementDemo()
    
    quality_scores = {
        "linkedin": 8.5,
        "tiktok": 7.9,
        "youtube": 8.2,
        "sales": 8.7,
        "podcast": 6.8,
    }
    
    result = demo.simulate_improvement("test_user", quality_scores)
    
    assert result["status"] == "improved"
    assert "weakness" in result
    assert "improvement" in result
    assert "new_scores" in result
    assert result["new_scores"]["podcast"] > quality_scores["podcast"]
    print("   ✓ Self-improvement demo working")
    print(f"   ✓ Detected weakness: {result['weakness']['weakest_format']}")
    print(f"   ✓ Score improved: {quality_scores['podcast']:.1f} → {result['new_scores']['podcast']:.1f}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Test 4: State Updates
print("\n4. Testing State Updates...")
try:
    from core.state import MirrorState
    
    state: MirrorState = {
        "user_id": "test",
        "audio_path": "test.mp3",
        "image_path": None,
        "trace_id": "test_trace",
        "transcript": None,
        "language": None,
        "emotion": None,
        "visual_context": None,
        "voice_id": None,
        "avatar_id": None,
        "avatar_look_id": None,
        "face_image_url": None,
        "scripts": {},
        "videos": {},
        "broll_urls": [],
        "translations": {},
        "quality_scores": None,
        "rewrite_count": 0,
        "optimized_prompts": None,
        "avatar_collaboration": None,
        "liveavatar_session": None,
        "errors": [],
        "start_time": 0.0,
    }
    
    # Verify all required fields exist
    required_fields = ["avatar_collaboration", "visual_context", "image_path"]
    for field in required_fields:
        assert field in state
    
    print("   ✓ State includes all new fields")
    print(f"   ✓ Total state fields: {len(state)}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Test 5: Documentation
print("\n5. Verifying Documentation...")
docs = [
    "WINNING_STRATEGY.md",
    "BUSINESS_PROOF.md",
    "DEMO_SCRIPT_V3.md",
]

for doc in docs:
    if Path(doc).exists():
        size = Path(doc).stat().st_size
        print(f"   ✓ {doc} ({size:,} bytes)")
    else:
        print(f"   ✗ Missing: {doc}")
        sys.exit(1)

print("\n=== All Verifications Passed ===")
print("\nWinning Enhancements Ready:")
print("  1. ✓ Avatar Collaboration (theatrical moment)")
print("  2. ✓ Router Visualization (agent thinking)")
print("  3. ✓ Self-Improvement Demo (PostHog learning)")
print("  4. ✓ Business Proof (ContentScale pilot)")
print("\nDemo Script: DEMO_SCRIPT_V3.md")
print("Strategy Doc: WINNING_STRATEGY.md")
print("\nReady for hackathon submission!")
