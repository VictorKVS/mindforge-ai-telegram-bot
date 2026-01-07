from src.core.audit.db import audit_db

session = audit_db.start_session(
    user_id=1,
    username="viktor",
    mode="DEMO",
    trust_level=0,
    state="start",
)

audit_db.log_event(
    session_id=session,
    user_id=1,
    username="viktor",
    event_type="UI_EVENT",
    action="demo_start",
    state="start",
    decision="INFO",
    policy="DEMO",
    source="ADR-0001",
    payload={"entry": "/start"},
)

audit_db.log_event(
    session_id=session,
    user_id=1,
    username="viktor",
    event_type="POLICY",
    action="action_blocked",
    decision="DENY",
    policy="UAG",
    source="RULE-TRUST-01",
    payload={"reason": "no_autonomy"},
)

print("AUDIT LEDGER OK")
