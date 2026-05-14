"""Tests for MIRROR agents."""
import pytest
from unittest.mock import patch, MagicMock


class TestIntakeAgent:
    @patch("agents.intake.elevenlabs")
    @patch("agents.intake._llm")
    def test_intake_returns_transcript_and_emotion(self, mock_llm, mock_el):
        mock_el.transcribe.return_value = {
            "text": "Hello world",
            "language": "en",
            "words": []
        }
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '{"emotion": "confident"}'
        mock_response.usage.prompt_tokens = 100
        mock_response.usage.completion_tokens = 50
        mock_llm.chat.completions.create.return_value = mock_response

        from agents.intake import run
        state = {"user_id": "test", "audio_path": "test.mp3", "errors": []}
        result = run(state)

        assert result["transcript"] == "Hello world"
        assert result["emotion"] == "confident"
