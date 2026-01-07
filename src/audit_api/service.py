from typing import List, Dict, Any
from src.core.audit.db import AuditDB


def list_sessions(db: AuditDB, limit: int = 50) -> List[Dict]:
    with db._conn() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM sessions
            ORDER BY started_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(r) for r in rows]


def get_session_timeline(db: AuditDB, session_id: str) -> List[Dict]:
    with db._conn() as conn:
        rows = conn.execute(
            """
            SELECT
                ts,
                event_type,
                action,
                state,
                decision,
                policy,
                source,
                payload
            FROM audit_events
            WHERE session_id = ?
            ORDER BY ts
            """,
            (session_id,),
        ).fetchall()

    result = []
    for r in rows:
        item = dict(r)
        if item.get("payload"):
            import json
            item["payload"] = json.loads(item["payload"])
        else:
            item["payload"] = {}
        result.append(item)

    return result


def explain_session(db: AuditDB, session_id: str) -> Dict[str, Any]:
    """
    WHY API — краткое объяснение, что происходило
    """
    timeline = get_session_timeline(db, session_id)

    summary = {
        "session_id": session_id,
        "total_events": len(timeline),
        "denies": 0,
        "allows": 0,
        "policies_triggered": set(),
    }

    for e in timeline:
        if e.get("decision") == "DENY":
            summary["denies"] += 1
        if e.get("decision") == "ALLOW":
            summary["allows"] += 1
        if e.get("policy"):
            summary["policies_triggered"].add(e["policy"])

    summary["policies_triggered"] = list(summary["policies_triggered"])
    summary["explanation"] = (
        "Система работала в контролируемом режиме. "
        "Все действия проходили через политики и FSM."
    )

    return summary
