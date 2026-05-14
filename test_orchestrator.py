"""Tests for orchestrator."""
import pytest
from core.orchestrator import route_by_quality


def test_route_by_quality_proceeds_when_all_scores_above_7():
    state = {"quality_scores": {"linkedin": 8.0, "tiktok": 7.5}, "rewrite_count": 0}
    assert route_by_quality(state) == "proceed"


def test_route_by_quality_rewrites_when_score_below_7():
    state = {"quality_scores": {"linkedin": 6.0, "tiktok": 8.0}, "rewrite_count": 0}
    assert route_by_quality(state) == "rewrite"


def test_route_by_quality_proceeds_after_max_rewrites():
    state = {"quality_scores": {"linkedin": 6.0}, "rewrite_count": 2}
    assert route_by_quality(state) == "proceed"
