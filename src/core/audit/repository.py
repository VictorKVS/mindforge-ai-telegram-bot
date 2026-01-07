from datetime import datetime
from typing import Optional

from src.core.audit.db import get_connection


class AuditRepository:
    @staticmethod
    def log_ui_event(
        *,
        user_id: int,
        username: Optional[str],
        chat_id: int,
        action: str,
        state: Optional[str],
        source: str = "telegram-bot",
    ) -> None:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO ui_events (
                timestamp,
                user_id,
                username,
                chat_id,
                action,
                state,
                source
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.utcnow().isoformat(),
                user_id,
                username,
                chat_id,
                action,
                state,
                source,
            ),
        )

        conn.commit()
        conn.close()
