# src/polygon/scenario_yaml_loader.py

from pathlib import Path
import yaml

SCENARIO_DIR = Path("src/polygon/scenarios")


def load_all_yaml_scenarios() -> list[dict]:
    scenarios = []

    for file in SCENARIO_DIR.glob("*.yaml"):
        with open(file, "r", encoding="utf-8") as f:
            scenarios.append(yaml.safe_load(f))

    return scenarios


def load_last_yaml_scenario() -> dict | None:
    files = sorted(
        SCENARIO_DIR.glob("*.yaml"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if not files:
        return None

    with open(files[0], "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
