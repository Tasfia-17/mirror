"""ElevenLabs client -- transcribe, instant voice clone, TTS."""
from io import BytesIO
from elevenlabs.client import ElevenLabs
from config import ELEVENLABS_API_KEY

_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)


def transcribe(audio_path: str) -> dict:
    """Transcribe audio with Scribe v2. Returns {text, words, language}."""
    with open(audio_path, "rb") as f:
        result = _client.speech_to_text.convert(
            file=f,
            model_id="scribe_v2",
            tag_audio_events=True,
            diarize=False,
        )
    return {"text": result.text, "words": result.words, "language": result.language_code}


def clone_voice(audio_path: str, name: str = "mirror_voice") -> str:
    """Instant voice clone from audio file. Returns voice_id."""
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()

    voice = _client.voices.ivc.create(
        name=name,
        files=[BytesIO(audio_bytes)],
    )
    return voice.voice_id


def text_to_speech(text: str, voice_id: str, output_path: str) -> str:
    """Generate TTS audio. Returns output_path."""
    audio = _client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)
    return output_path
__all__ = ['transcribe', 'clone_voice', 'text_to_speech']
