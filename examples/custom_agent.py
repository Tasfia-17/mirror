"""Example of adding a custom agent to the pipeline."""
from core.state import MirrorState

def custom_agent(state: MirrorState) -> MirrorState:
    """Custom agent that adds metadata."""
    state["custom_field"] = "custom_value"
    return state

# Add to orchestrator by modifying create_graph()
