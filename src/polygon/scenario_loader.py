import yaml
from pathlib import Path

SCENARIOS_DIR = Path("src/polygon/scenarios")


def load_scenario(scenario_id: str) -> dict:
    path = SCENARIOS_DIR / f"{scenario_id}.yaml"
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
