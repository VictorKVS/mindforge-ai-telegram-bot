import json
from datetime import datetime
from pathlib import Path

AUDIT_LOG = Path("src/uag/audit.log")


def log_decision(agent_id: str, intent: str, decision: str, env: str):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "agent_id": agent_id,
        "intent": intent,
        "decision": decision,
        "env": env
    }
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
