from fastapi import FastAPI, Depends, HTTPException
from src.audit_api.deps import get_audit_db
from src.audit_api import service
from src.audit_api.schemas import SessionOut, AuditEventOut

app = FastAPI(
    title="MindForge Audit API",
    description="Read-only audit ledger (L1)",
    version="1.0",
)


@app.get("/sessions", response_model=list[SessionOut])
def sessions(limit: int = 50, db=Depends(get_audit_db)):
    return service.list_sessions(db, limit)


@app.get("/sessions/{session_id}/timeline", response_model=list[AuditEventOut])
def timeline(session_id: str, db=Depends(get_audit_db)):
    events = service.get_session_timeline(db, session_id)
    if not events:
        raise HTTPException(status_code=404, detail="Session not found")
    return events


@app.get("/sessions/{session_id}/why")
def why(session_id: str, db=Depends(get_audit_db)):
    explanation = service.explain_session(db, session_id)
    if explanation["total_events"] == 0:
        raise HTTPException(status_code=404, detail="Session not found")
    return explanation
