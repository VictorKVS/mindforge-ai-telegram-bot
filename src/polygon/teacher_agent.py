# src/polygon/teacher_agent.py

import json
import yaml
from datetime import datetime
from pathlib import Path
from src.agents.bootstrapper import bootstrap_agent_from_scenario

AUDIT_LOG = Path("src/uag/audit.log")
SCENARIO_DIR = Path("src/polygon/scenarios")
SCENARIO_DIR.mkdir(parents=True, exist_ok=True)


class TeacherAgent:
    def __init__(self):
        self.buffer = []

    def read_audit_log(self):
        if not AUDIT_LOG.exists():
            return []

        with open(AUDIT_LOG, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]

    def group_by_agent(self, records):
        grouped = {}
        for r in records:
            grouped.setdefault(r["agent_id"], []).append(r)
        return grouped

    def build_scenario(self, agent_id: str, records: list) -> dict:
        steps = []

        for i, r in enumerate(records, start=1):
            steps.append({
                "step": i,
                "actor": agent_id,
                "intent": r["intent"],
                "decision": r["decision"].lower(),
                "env": r["env"]
            })

        scenario = {
            "scenario_id": f"{agent_id}_scenario_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "source": "audit_log",
            "created_at": datetime.utcnow().isoformat(),
            "actors": [
                {"id": agent_id}
            ],
            "steps": steps,
            "learning_notes": self.infer_learning(records)
        }

        return scenario

    def infer_learning(self, records: list) -> list:
        notes = []
        intents = {r["intent"] for r in records}

        if "build_foundation" in intents:
            notes.append("Agent can execute build_foundation when RBAC allows")

        if any(r["decision"] == "DENY" for r in records):
            notes.append("RBAC denied some intents — check permissions")

        return notes

    def write_scenario(self, scenario: dict):
        path = SCENARIO_DIR / f"{scenario['scenario_id']}.yaml"
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(scenario, f, allow_unicode=True)

    def run(self):
        records = self.read_audit_log()
        grouped = self.group_by_agent(records)

        for agent_id, agent_records in grouped.items():
            scenario = self.build_scenario(agent_id, agent_records)
            self.write_scenario(scenario)
        
        agent_id = bootstrap_agent_from_scenario(
        scenario,
        role="shop"  # или builder / student
        )
