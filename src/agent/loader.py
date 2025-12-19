# src/agents/loader.py


from pathlib import Path
import yaml

AGENT_REGISTRY = Path("src/agents/registry")


class AgentNotFound(Exception):
    pass


def load_agent_spec(agent_id: str) -> dict:
    """
    Загружает AgentSpec.yaml по agent_id
    """
    path = AGENT_REGISTRY / f"{agent_id}.yaml"

    if not path.exists():
        raise AgentNotFound(f"AgentSpec not found: {agent_id}")

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
