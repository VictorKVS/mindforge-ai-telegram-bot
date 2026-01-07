from src.core.audit.db import get_connection

def migrate():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ui_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        action TEXT NOT NULL,
        state TEXT,
        source TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("[AUDIT] Migration complete")


if __name__ == "__main__":
    migrate()
