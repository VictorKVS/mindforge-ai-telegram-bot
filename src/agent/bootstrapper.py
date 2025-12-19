# src/agents/bootstrapper.py

import json
from datetime import datetime
from pathlib import Path

AGENT_DIR = Path("src/agents/instances")
AGENT_DIR.mkdir(parents=True, exist_ok=True)


def bootstrap_agent_from_scenario(scenario: dict, role: str):
    agent_id = scenario["actors"][0]["id"] + "_clone"

    agent = {
        "agent_id": agent_id,
        "role": role,
        "level": 1,
        "skills": [],
        "allowed_intents": [],
        "learned_from": [scenario["scenario_id"]],
        "created_at": datetime.utcnow().isoformat()
    }

    for step in scenario["steps"]:
        if step["decision"] == "allowed":
            agent["allowed_intents"].append(step["intent"])

    agent["allowed_intents"] = sorted(set(agent["allowed_intents"]))

    path = AGENT_DIR / f"{agent_id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(agent, f, indent=2, ensure_ascii=False)

    return agent_id
