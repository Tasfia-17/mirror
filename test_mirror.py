"""Tests for MIRROR clients using mocks."""
import json
import pytest
from unittest.mock import patch, MagicMock, mock_open


class TestElevenLabsClient:
    @patch("clients.elevenlabs._client")
    def test_transcribe_returns_text_and_language(self, mock_client):
        mock_result = MagicMock()
        mock_result.text = "Hello world"
        mock_result.words = []
        mock_result.language_code = "en"
        mock_client.speech_to_text.convert.return_value = mock_result

        from clients.elevenlabs import transcribe
        with patch("builtins.open", mock_open(read_data=b"audio")):
            result = transcribe("test.mp3")

        assert result["text"] == "Hello world"
        assert result["language"] == "en"

    @patch("clients.elevenlabs._client")
    def test_clone_voice_returns_voice_id(self, mock_client):
        mock_voice = MagicMock()
        mock_voice.voice_id = "voice_abc123"
        mock_client.voices.ivc.create.return_value = mock_voice

        from clients.elevenlabs import clone_voice
        with patch("builtins.open", mock_open(read_data=b"audio")):
            voice_id = clone_voice("test.mp3", "test_voice")

        assert voice_id == "voice_abc123"


class TestPostHogClient:
    @patch("clients.posthog_client._client")
    def test_capture_calls_posthog(self, mock_client):
        from clients.posthog_client import capture
        capture("user_1", "test_event", {"key": "value"})
        mock_client.capture.assert_called_once_with(
            "user_1", "test_event", properties={"key": "value"}
        )

    @patch("clients.posthog_client._client")
    def test_track_llm_uses_ai_generation_event(self, mock_client):
        from clients.posthog_client import track_llm
        track_llm("user_1", "gpt-4o-mini", 100, 50, 1200.0, "test_step")
        call_args = mock_client.capture.call_args
        assert call_args[0][1] == "$ai_generation"
        props = call_args[1]["properties"]
        assert props["$ai_model"] == "gpt-4o-mini"
        assert props["$ai_input_tokens"] == 100
        assert props["$ai_output_tokens"] == 50


class TestRetry:
    def test_with_retry_succeeds_on_first_attempt(self):
        from core.retry import with_retry
        call_count = 0

        @with_retry(max_attempts=3, base_delay=0.01)
        def succeed():
            nonlocal call_count
            call_count += 1
            return "ok"

        result = succeed()
        assert result == "ok"
        assert call_count == 1

    def test_with_retry_retries_on_failure(self):
        from core.retry import with_retry
        call_count = 0

        @with_retry(max_attempts=3, base_delay=0.01)
        def fail_twice():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("transient error")
            return "ok"

        result = fail_twice()
        assert result == "ok"
        assert call_count == 3

    def test_with_retry_raises_after_max_attempts(self):
        from core.retry import with_retry

        @with_retry(max_attempts=2, base_delay=0.01)
        def always_fail():
            raise RuntimeError("permanent error")

        with pytest.raises(RuntimeError, match="permanent error"):
            always_fail()


class TestCostCalculator:
    def test_calculate_generation_cost_returns_positive_total(self):
        from core.cost import calculate_generation_cost
        # 60s input, 30s output, 5 formats, 10 languages — full pipeline
        cost = calculate_generation_cost(60, 30, 5, 10)
        assert cost["total"] > 0
        assert cost["total"] < 30  # sanity check: full pipeline under $30
        assert cost["formats"] == 5
        assert cost["languages"] == 10

    def test_calculate_margin_pro_tier(self):
        from core.cost import calculate_margin
        # Pro tier: $199/mo. At ~$20/generation, 5 generations = ~$102 cost → positive margin.
        margin = calculate_margin("pro", 5)
        assert margin["revenue"] == 199
        assert margin["margin_pct"] > 0


class TestConfig:
    def test_require_raises_on_missing_env_var(self):
        import os
        from config import _require
        if "NONEXISTENT_VAR" in os.environ:
            del os.environ["NONEXISTENT_VAR"]
        with pytest.raises(EnvironmentError, match="Missing required"):
            _require("NONEXISTENT_VAR")
