import sqlite3
import json
import uuid
from typing import List, Dict, Any, Optional
from pathlib import Path
from contextlib import contextmanager
from datetime import datetime

DB_PATH = "data/audit.db"
SCHEMA_PATH = "src/core/audit/schema.sql"


class AuditDB:
    """
    L1 Audit Ledger (append-only)
    Единая точка записи и чтения аудита
    """

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with self._conn() as conn:
            with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
                conn.executescript(f.read())

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row

        # Ledger guarantees
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA foreign_keys=ON;")

        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    # =====================================================
    # SESSION
    # =====================================================
    def start_session(
        self,
        user_id: int,
        username: str,
        mode: str = "DEMO",
        trust_level: int = 0,
        state: Optional[str] = None,
    ) -> str:
        session_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()

        with self._conn() as conn:
            conn.execute(
                """
                INSERT INTO sessions
                (session_id, user_id, username, started_at, last_state, trust_level, mode)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    user_id,
                    username,
                    now,
                    state,
                    trust_level,
                    mode,
                ),
            )

        return session_id

    def update_state(self, session_id: str, state: str):
        with self._conn() as conn:
            conn.execute(
                "UPDATE sessions SET last_state=? WHERE session_id=?",
                (state, session_id),
            )

    # =====================================================
    # AUDIT EVENT (WRITE PATH)
    # =====================================================
    def log_event(
        self,
        *,
        session_id: str,
        user_id: int,
        username: str,
        event_type: str,
        action: str,
        state: Optional[str] = None,
        decision: Optional[str] = None,
        policy: Optional[str] = None,
        source: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
    ):
        now = datetime.utcnow().isoformat()

        with self._conn() as conn:
            conn.execute(
                """
                INSERT INTO audit_events
                (
                    ts, user_id, username, session_id,
                    event_type, action, state,
                    decision, policy, source,
                    payload
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    now,
                    user_id,
                    username,
                    session_id,
                    event_type,
                    action,
                    state,
                    decision,
                    policy,
                    source,
                    json.dumps(payload or {}, ensure_ascii=False),
                ),
            )

    # =====================================================
    # READ API
    # =====================================================
    def get_last_session_for_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        with self._conn() as conn:
            row = conn.execute(
                """
                SELECT *
                FROM sessions
                WHERE user_id = ?
                ORDER BY started_at DESC
                LIMIT 1
                """,
                (user_id,),
            ).fetchone()

        return dict(row) if row else None

    def get_events(self, session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        with self._conn() as conn:
            rows = conn.execute(
                """
                SELECT ts, event_type, action, state, decision, policy, source, payload
                FROM audit_events
                WHERE session_id = ?
                ORDER BY ts DESC
                LIMIT ?
                """,
                (session_id, limit),
            ).fetchall()

        events: List[Dict[str, Any]] = []
        for r in rows:
            item = dict(r)
            try:
                item["payload"] = json.loads(item["payload"]) if item["payload"] else {}
            except Exception:
                item["payload"] = {"_raw": item.get("payload")}
            events.append(item)

        return events[::-1]

    def get_sessions(self, limit: int = 20) -> List[Dict[str, Any]]:
        with self._conn() as conn:
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

    # =====================================================
    # SESSION REPLAY (READ ONLY)
    # =====================================================
    def get_session_timeline(self, session_id: str) -> List[Dict[str, Any]]:
        with self._conn() as conn:
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
                ORDER BY ts ASC
                """,
                (session_id,),
            ).fetchall()

        timeline: List[Dict[str, Any]] = []
        for r in rows:
            item = dict(r)
            try:
                item["payload"] = json.loads(item["payload"]) if item["payload"] else {}
            except Exception:
                item["payload"] = {"_raw": item.get("payload")}
            timeline.append(item)

        return timeline


# ГЛОБАЛЬНЫЙ LEDGER
audit_db = AuditDB()
