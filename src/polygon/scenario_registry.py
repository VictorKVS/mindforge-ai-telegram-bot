# src/polygon/scenario_registry.py

from pathlib import Path
import yaml


SCENARIO_DIR = Path("src/polygon/scenarios")


class ScenarioRegistry:
    @staticmethod
    def yaml_all() -> list[dict]:
        if not SCENARIO_DIR.exists():
            return []

        files = sorted(
            SCENARIO_DIR.glob("*.yaml"),
            key=lambda p: p.stat().st_mtime
        )

        scenarios = []
        for f in files:
            try:
                with open(f, "r", encoding="utf-8") as fh:
                    scenarios.append(yaml.safe_load(fh))
            except Exception:
                continue

        return scenarios

    @staticmethod
    def yaml_last() -> dict | None:
        all_yaml = ScenarioRegistry.yaml_all()
        return all_yaml[-1] if all_yaml else None
