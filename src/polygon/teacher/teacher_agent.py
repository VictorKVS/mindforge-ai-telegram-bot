# src/polygon/teacher/teacher_agent.py


from pathlib import Path
from datetime import datetime, timezone
import yaml
import uuid

# Где лежат сценарии
SCENARIO_DIR = Path("src/polygon/scenarios")

# Простая карта: intent → agent
INTENT_AGENT_MAP = {
    "build_foundation": "BuilderAgent",
    "get_price": "ShopAgent",
    "send_offer": "ShopAgent",
}

class TeacherAgent:
    """
    Teacher Agent:
    - читает последний YAML-сценарий
    - обогащает его (назначает agent)
    - сохраняет новую версию
    """

    def list_knowledge(self) -> list[str]:
        """Список доступных knowledge-блоков (пока заглушка)"""
        return ["bricks_quality_v1"]

    def teach(self) -> dict | None:
        last = self._load_last_scenario()
        if not last:
            return None

        enriched = self._enrich_scenario(last)
        self._save_scenario(enriched)
        return enriched

    # -------------------------
    # ВНУТРЕННИЕ МЕТОДЫ
    # -------------------------

    def _load_last_scenario(self) -> dict | None:
        if not SCENARIO_DIR.exists():
            return None

        files = sorted(
            SCENARIO_DIR.glob("*.yaml"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )

        if not files:
            return None

        with open(files[0], "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _enrich_scenario(self, scenario: dict) -> dict:
        new_scenario = dict(scenario)

        new_scenario["scenario_id"] = (
            scenario.get("scenario_id", "scenario") + "_trained"
        )

        new_scenario["created_at"] = datetime.now(timezone.utc).isoformat()

        steps = []
        for step in scenario.get("steps", []):
            intent = step.get("intent")
            agent = INTENT_AGENT_MAP.get(intent, "UnknownAgent")

            steps.append({
                "intent": intent,
                "agent": agent,
                "decision": step.get("decision", "ALLOW"),
            })

        new_scenario["steps"] = steps
        return new_scenario

    def _save_scenario(self, scenario: dict):
        SCENARIO_DIR.mkdir(parents=True, exist_ok=True)

        fname = f"{scenario['scenario_id']}_{uuid.uuid4().hex[:6]}.yaml"
        path = SCENARIO_DIR / fname

        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(
                scenario,
                f,
                allow_unicode=True,
                sort_keys=False
            )
