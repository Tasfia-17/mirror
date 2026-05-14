"""Example of customizing format guidelines."""
from config import FORMATS
from core.prompts import FORMAT_GUIDELINES

# Override guidelines for a specific format
FORMAT_GUIDELINES["linkedin"] = "Professional but conversational. Start with a question."

# Then run the pipeline as usual
from core.orchestrator import run_pipeline
result = run_pipeline("voice_memo.mp3")
