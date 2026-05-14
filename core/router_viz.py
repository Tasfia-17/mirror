"""Agent Router Visualization -- real-time graph showing agent execution flow."""
import json
import time
from typing import Dict, List
from core.state import MirrorState


class AgentRouterViz:
    """Tracks and visualizes agent execution in real-time."""
    
    def __init__(self):
        self.events: List[Dict] = []
        self.start_time = time.time()
    
    def log_agent_start(self, agent_name: str, state: MirrorState):
        """Log when an agent starts execution."""
        self.events.append({
            "type": "agent_start",
            "agent": agent_name,
            "timestamp": time.time() - self.start_time,
            "state_keys": list(state.keys()),
        })
    
    def log_agent_complete(self, agent_name: str, duration_ms: float, success: bool):
        """Log when an agent completes."""
        self.events.append({
            "type": "agent_complete",
            "agent": agent_name,
            "timestamp": time.time() - self.start_time,
            "duration_ms": duration_ms,
            "success": success,
        })
    
    def log_routing_decision(self, from_agent: str, to_agent: str, reason: str):
        """Log routing decisions (e.g., Critic loop back)."""
        self.events.append({
            "type": "routing_decision",
            "from": from_agent,
            "to": to_agent,
            "reason": reason,
            "timestamp": time.time() - self.start_time,
        })
    
    def log_cost(self, agent_name: str, cost_usd: float):
        """Log cost per agent."""
        self.events.append({
            "type": "cost",
            "agent": agent_name,
            "cost_usd": cost_usd,
            "timestamp": time.time() - self.start_time,
        })
    
    def get_graph_data(self) -> dict:
        """Return graph visualization data."""
        nodes = []
        edges = []
        costs = {}
        
        agent_order = ["intake", "identity", "format", "critic", "cinematic", "hyperframes", "translate", "optimizer"]
        
        for i, agent in enumerate(agent_order):
            status = "pending"
            duration = 0
            
            # Check if agent has completed
            for event in self.events:
                if event["type"] == "agent_complete" and event["agent"] == agent:
                    status = "complete" if event["success"] else "error"
                    duration = event["duration_ms"]
                elif event["type"] == "agent_start" and event["agent"] == agent:
                    status = "running"
            
            nodes.append({
                "id": agent,
                "label": agent.title(),
                "status": status,
                "duration_ms": duration,
                "position": {"x": 100 + i * 120, "y": 200},
            })
        
        # Build edges
        for i in range(len(agent_order) - 1):
            edges.append({
                "from": agent_order[i],
                "to": agent_order[i + 1],
                "type": "normal",
            })
        
        # Add routing decisions (e.g., Critic loop)
        for event in self.events:
            if event["type"] == "routing_decision":
                edges.append({
                    "from": event["from"],
                    "to": event["to"],
                    "type": "conditional",
                    "reason": event["reason"],
                })
        
        # Aggregate costs
        for event in self.events:
            if event["type"] == "cost":
                costs[event["agent"]] = costs.get(event["agent"], 0) + event["cost_usd"]
        
        return {
            "nodes": nodes,
            "edges": edges,
            "costs": costs,
            "total_cost": sum(costs.values()),
            "events": self.events,
        }
    
    def export_json(self, path: str):
        """Export visualization data to JSON file."""
        with open(path, "w") as f:
            json.dump(self.get_graph_data(), f, indent=2)


# Global instance for tracking
_router_viz = AgentRouterViz()


def get_router_viz() -> AgentRouterViz:
    """Get the global router visualization instance."""
    return _router_viz


def reset_router_viz():
    """Reset the router visualization for a new run."""
    global _router_viz
    _router_viz = AgentRouterViz()
