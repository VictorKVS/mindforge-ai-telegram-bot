-- =========================================================
-- MindForge Audit Ledger (L1)
-- =========================================================

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- ---------------------------------------------------------
-- СЕССИИ
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    username TEXT,
    started_at TEXT NOT NULL,
    last_state TEXT,
    trust_level INTEGER,
    mode TEXT              -- DEMO | PROD
);

-- ---------------------------------------------------------
-- АУДИТ СОБЫТИЙ (ЕДИНАЯ ЛЕНТА)
-- ---------------------------------------------------------
CREATE TABLE IF NOT EXISTS audit_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,

    user_id INTEGER,
    username TEXT,
    session_id TEXT,

    event_type TEXT NOT NULL,    -- UI_EVENT | FSM | POLICY | AGENT | EXPLAIN
    action TEXT NOT NULL,        -- demo_start | activate_pro | why_dashboard
    state TEXT,                  -- dashboard | activation | scenario

    decision TEXT,               -- ALLOW | DENY | INFO
    policy TEXT,                 -- TRUST | UAG | PAYMENT | DEMO
    source TEXT,                 -- ADR-0002 | RULE-TRUST-01

    payload TEXT,                -- JSON

    FOREIGN KEY(session_id) REFERENCES sessions(session_id)
);

-- ---------------------------------------------------------
-- ИНДЕКСЫ
-- ---------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_audit_ts
    ON audit_events(ts);

CREATE INDEX IF NOT EXISTS idx_audit_user
    ON audit_events(user_id);

CREATE INDEX IF NOT EXISTS idx_audit_session
    ON audit_events(session_id);

CREATE INDEX IF NOT EXISTS idx_audit_event
    ON audit_events(event_type, action);
