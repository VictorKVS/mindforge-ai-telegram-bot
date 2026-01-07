AISOC Core — L2 Architecture (Text Diagram)

┌────────────────────────────────────────────────────────────┐
│                        External World                      │
│         (Telegram, Web UI, External Agents, APIs)          │
└───────────────▲───────────────────────────▲────────────────┘
                │                           │
        User Intent / Request        External Agent Call
                │                           │
                └───────────────┬───────────┘
                                │
                    ┌───────────▼───────────┐
                    │   Decision Layer      │
                    │ (Runtime Orchestrator)│
                    └───────────┬───────────┘
                                │
                ┌───────────────▼────────────────┐
                │        AISOC CORE              │
                │--------------------------------│
                │ 1. Agent Registry              │
                │ 2. Trust Level Resolver        │
                │ 3. Policy Engine (OPA/Rego)    │
                │ 4. Runtime Enforcement Point   │
                │ 5. Risk Scoring Engine         │
                │ 6. Reaction Controller         │
                └───────────┬───────────┬────────┘
                            │           │
            Allowed & Scoped│           │Denied / Risky
             Request        │           │
                            │           ▼
                            │   ┌─────────────────────┐
                            │   │ Incident / SOC Flow │
                            │   │ - Alert             │
                            │   │ - Escalation        │
                            │   │ - Kill / Degrade    │
                            │   └─────────────────────┘
                            │
          ┌─────────────────▼─────────────────┐
          │        Connector Security Layer   │
          │-----------------------------------│
          │ - No direct DB/API access         │
          │ - Query rewriting                 │
          │ - Data masking / filtering        │
          │ - Region & policy enforcement     │
          └───────────┬───────────┬───────────┘
                      │           │
        ┌─────────────▼───┐   ┌───▼────────────┐
        │Internal Systems │   │ External APIs  │
        │ (DB, 1C, CRM)   │   │ / Agents       │
        └─────────────────┘   └────────────────┘

──────────────────────────────────────────────────────────────

AUDIT & EXPLAINABILITY (SIDE PLANE)

For every action:
- Request context
- Agent identity & trust level
- Policy decision (ALLOW / DENY / TRANSFORM)
- Risk score
- Final response
- Explanation ("why")

Stored in:
- Immutable Audit Log
- Explainability Store

1. Что принципиально меняется в L2 (AISOC Core)
Было (L0/L1)	Стало (L2)
Бот → логика	Агент → Control Plane
Проверки “по месту”	Централизованное enforcement
Лог как побочный эффект	Audit как обязательный артефакт
Ответ = результат	Ответ = результат + объяснение
Ошибка = баг	Ошибка = инцидент
Агент “доверенный”	Агент = zero trust

👉 Ключ:
в L2 агент больше ничего не может напрямую.
Он просит, AISOC решает.

2. Ключевые свойства L2 
🔐 Zero Trust Agent Model

агент никогда не доверенный

даже “внутренний”

🧠 Policy-Driven Runtime

правила вне кода

политики — декларативные

легко аудитятся

🧾 Audit by Design

если нет лога → действия не было

explainability — не опция

🔥 Реакции — часть архитектуры

deny

degrade

isolate

escalate

kill-switch

3. Связь с ADR (обязательно)

Добавь в каждый ADR:

ADR-0001
## Architecture Reference
- L2 AISOC Core:
  - docs/diagrams/architecture/AISOC_L2_Core.md

ADR-0003 / 0006 / 0007

Ссылку на тот же файл — это важно:
👉 одна каноническая схема

5️⃣ Что делать с текущей схемой бота

Оставляем. Но чётко позиционируем:

mindforge_ai_telegram_bot_shema__7.md
→ L0/L1: UX & scenario validation
AISOC_L2_Core.md
→ L2: production security architecture


Это очень сильный ход:

ты не “переделываешь”,

ты эволюционируешь архитектуру.

6️⃣ Итог (коротко, как для Раниса)

L2 — это момент, когда агент перестаёт быть программой
и становится субъектом контроля.
AISOC — это не модуль, а нервная система всей платформы.