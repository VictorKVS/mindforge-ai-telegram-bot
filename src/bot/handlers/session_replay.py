import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from src.core.audit.db import audit_db

log = logging.getLogger("mindforge.replay")

router = Router()


# =====================================================
# 6.2 — СТАРТ SESSION REPLAY
# =====================================================
@router.callback_query(F.data == "session_replay")
async def session_replay_start(call: CallbackQuery):
    await call.answer()

    session = audit_db.get_last_session_for_user(call.from_user.id)
    if not session:
        await call.message.answer("❌ Нет сессий для воспроизведения")
        return

    session_id = session["session_id"]
    timeline = audit_db.get_session_timeline(session_id)

    await call.message.answer(
        f"▶️ *Session Replay*\n\n"
        f"Сессия: `{session_id}`\n"
        f"Событий: {len(timeline)}\n\n"
        f"Нажмите ▶️ для пошагового воспроизведения",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="▶️ Шаг 1",
                        callback_data=f"replay_step_0:{session_id}",
                    )
                ]
            ]
        ),
    )


# =====================================================
# 6.3 — ПОШАГОВОЕ ВОСПРОИЗВЕДЕНИЕ
# =====================================================
@router.callback_query(F.data.startswith("replay_step_"))
async def replay_step(call: CallbackQuery):
    await call.answer()

    raw = call.data.replace("replay_step_", "")
    step_str, session_id = raw.split(":")
    step = int(step_str)

    timeline = audit_db.get_session_timeline(session_id)

    if step >= len(timeline):
        await call.message.answer("✅ Replay завершён")
        return

    e = timeline[step]

    text = (
        f"🧭 *ШАГ {step + 1}/{len(timeline)}*\n\n"
        f"🕒 `{e['ts']}`\n"
        f"📌 *{e['event_type']}*\n"
        f"• action: `{e['action']}`\n"
        f"• state: `{e.get('state')}`\n"
        f"• decision: `{e.get('decision')}`\n"
        f"• policy: `{e.get('policy')}`\n"
        f"• source: `{e.get('source')}`\n"
    )

    if e.get("payload"):
        text += f"\n```json\n{e['payload']}\n```"

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="▶️ Далее",
                    callback_data=f"replay_step_{step + 1}:{session_id}",
                )
            ]
        ]
    )

    await call.message.answer(
        text,
        parse_mode="Markdown",
        reply_markup=kb,
    )

