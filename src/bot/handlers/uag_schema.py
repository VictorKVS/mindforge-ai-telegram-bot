import logging
import json
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from src.core.audit.db import audit_db

log = logging.getLogger("mindforge.uag")
router = Router()

# --- UI ---
def uag_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Показать живые логи", callback_data="show_live_logs")],
            [InlineKeyboardButton(text="🧩 Пример из БД (ledger)", callback_data="show_db_example")],
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_demo")],
        ]
    )

UAG_SCHEMA_MD = """
🔐 *UAG СХЕМА — КОНТРОЛЬ ПРИНЯТИЯ РЕШЕНИЙ*

┌─────────────────┐
│ 👤 ПОЛЬЗОВАТЕЛЬ │
│   (Telegram)    │
└────────┬────────┘
         │  *audit_events: UI_EVENT*
         ▼
┌─────────────────┐
│   МАСТЕР-АГЕНТ   │
│  «анализ, план»  │
└────────┬────────┘
         │  *audit_events: AGENT*
         ▼
┌─────────────────┐
│ РЕКОМЕНДАЦИЯ/ПЛАН │
│ «что предлагает»  │
└────────┬────────┘
         │  *audit_events: POLICY*
         ▼
┌─────────────────┐
│ 👨‍💼 ЧЕЛОВЕК РЕШАЕТ │
│  «approve/deny»   │
└────────┬────────┘
         │
         ├───────────────┐
         ▼               ▼
┌─────────────────┐   ⛔ *DEMO LIMIT*
│   ИСПОЛНЕНИЕ    │   «заблокировано»
└─────────────────┘

*КЛЮЧЕВЫЕ ТОЧКИ КОНТРОЛЯ:*
1) Любой запрос фиксируется как `UI_EVENT`
2) Агент формирует только анализ/план: `AGENT`
3) Политики дают ALLOW/DENY/INFO: `POLICY`
4) Исполнение в DEMO блокируется: `policy=DEMO`, `decision=DENY`

*Ключевая фраза:*
Агент может только рекомендовать. Человек решает. DEMO сознательно блокирует исполнение. Всё аудируется.
"""

@router.callback_query(F.data == "why_dashboard")
async def show_uag_schema(call: CallbackQuery):
    user = call.from_user
    session = audit_db.get_last_session_for_user(user.id)

    # если сессии нет — создадим минимальную (чтобы было что логировать)
    if not session:
        sid = audit_db.start_session(
            user_id=user.id,
            username=user.username or "",
            mode="DEMO",
            trust_level=0,
            state="why_dashboard",
        )
        session_id = sid
    else:
        session_id = session["session_id"]
        audit_db.update_state(session_id, "why_dashboard")

    audit_db.log_event(
        session_id=session_id,
        user_id=user.id,
        username=user.username or "",
        event_type="EXPLAIN",
        action="why_dashboard",
        state="why_dashboard",
        decision="INFO",
        policy="UAG",
        source="ADR-0002",
        payload={"screen": "uag_schema"},
    )

    await call.message.answer(UAG_SCHEMA_MD, parse_mode="Markdown", reply_markup=uag_keyboard())
    await call.answer()


@router.callback_query(F.data == "show_live_logs")
async def show_live_logs(call: CallbackQuery):
    user = call.from_user
    session = audit_db.get_last_session_for_user(user.id)
    if not session:
        await call.message.answer("Пока нет сессий. Нажми сначала «Показать схему контроля (UAG)».")
        await call.answer()
        return

    session_id = session["session_id"]
    events = audit_db.get_events(session_id, limit=20)

    audit_db.log_event(
        session_id=session_id,
        user_id=user.id,
        username=user.username or "",
        event_type="UI_EVENT",
        action="show_live_logs",
        state=session.get("last_state"),
        decision="INFO",
        policy="UAG",
        source="UI",
        payload={"limit": 20},
    )

    lines = []
    for e in events:
        lines.append(
            f"• `{e['ts']}` | *{e['event_type']}* | `{e['action']}`"
            f"{' | ' + e['decision'] if e.get('decision') else ''}"
            f"{' | ' + e['policy'] if e.get('policy') else ''}"
        )

    text = (
        "📊 *Живые логи (последние 20 событий)*\n\n"
        f"*Session:* `{session_id}`\n\n" +
        "\n".join(lines)
    )

    await call.message.answer(text, parse_mode="Markdown")
    await call.answer()


@router.callback_query(F.data == "show_db_example")
async def show_db_example(call: CallbackQuery):
    user = call.from_user
    session = audit_db.get_last_session_for_user(user.id)
    if not session:
        await call.message.answer("Пока нет сессий. Открой сначала UAG схему.")
        await call.answer()
        return

    session_id = session["session_id"]

    example = {
        "sessions": {
            "session_id": session_id,
            "user_id": user.id,
            "mode": "DEMO",
            "trust_level": 0,
        },
        "audit_events_example": {
            "event_type": "POLICY",
            "action": "demo_block_execution",
            "decision": "DENY",
            "policy": "DEMO",
            "source": "RULE-DEMO-01",
            "payload": {"blocked_action": "purchase.execute"},
        },
    }

    audit_db.log_event(
        session_id=session_id,
        user_id=user.id,
        username=user.username or "",
        event_type="EXPLAIN",
        action="show_db_example",
        state=session.get("last_state"),
        decision="INFO",
        policy="UAG",
        source="UI",
        payload={"note": "shown_example"},
    )

    await call.message.answer(
        "🧩 *Пример записи в Audit Ledger*\n\n```json\n"
        + json.dumps(example, ensure_ascii=False, indent=2)
        + "\n```",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="◀️ Назад к схеме", callback_data="why_dashboard")]]
        ),
    )
    await call.answer()
