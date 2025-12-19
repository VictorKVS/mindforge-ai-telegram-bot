def format_scenario_for_telegram(s: dict) -> str:
    if not s:
        return "❌ Сценарий не найден."

    lines = []
    lines.append("🏗 <b>DEMO: Сценарий</b>\n")

    lines.append(f"<b>ID:</b> {s.get('scenario_id', '—')}")
    lines.append(f"<b>Created:</b> {s.get('created_at', '—')}\n")

    agents = s.get("agents", [])
    if agents:
        lines.append("<b>Агенты:</b>")
        for a in agents:
            lines.append(f"• <b>{a.get('id')}</b> — {a.get('role')}")
        lines.append("")

    steps = s.get("steps", [])
    if not steps:
        lines.append("Нет шагов.")
    else:
        lines.append("<b>Сценарий выполнения:</b>")
        for i, st in enumerate(steps, 1):
            lines.append(
                f"{i}. <b>{st.get('agent','—')}</b> → "
                f"<code>{st.get('intent','—')}</code> "
                f"({st.get('decision','—')})"
            )

    return "\n".join(lines)
