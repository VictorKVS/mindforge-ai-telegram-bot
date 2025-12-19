import json
from datetime import datetime
from pathlib import Path

AUDIT_LOG = Path("src/uag/audit.log")


def log_decision(record: dict):
    """
    Записывает audit event.
    Ожидает полностью сформированный record.
    """
    record["timestamp"] = datetime.utcnow().isoformat()

    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
