IMPLEMENTATION_PLAN_L3.md

📍 Путь в проекте:
docs/specs/ml3/implementation/IMPLEMENTATION_PLAN_L3.md

IMPLEMENTATION_PLAN_L3.md

MindForge · L3 Agent Interaction — Implementation Roadmap

1. Назначение

Данный документ определяет пошаговый план реализации уровня L3 — контролируемого межагентного взаимодействия — строго в соответствии с утверждёнными документами:

ARCH_AGENT_INTERACTION_L3.md

CONTRACT_AGENT_INTERACTION_L3.md

TEST_AGENT_INTERACTION_L3.md

PROCESS_POLYGON_CERTIFICATION_L3.md

Цель:
👉 получить минимальный, но полностью рабочий L3, проходящий сертификацию Polygon.

2. Общие правила реализации (обязательные)

❌ Никакой логики доступа в агентах

❌ Никаких прямых вызовов agent → agent

✅ Вся маршрутизация и фильтрация — только в UAG

✅ Код = реализация контрактов, не место для интерпретаций

✅ Каждый шаг имеет DoD (Definition of Done)

3. Порядок реализации (строгий)
STEP 1 — Fake Agent Provider (Agent B)

📌 Цель: создать изолированного provider’а, представляющего Agent B

📂 Файлы:

src/providers/fake_agent_provider.py


📋 Функции:

register_agent(agent_id)

expose_capability(capability_contract)

execute_capability(capability_name)

📌 Особенности:

Agent B не знает, кто вызывает

Agent B не проверяет права

Возвращает полный объект, фильтрация будет в UAG

✅ DoD:

Provider возвращает данные по capability

Нет проверок доступа внутри provider

STEP 2 — Capability Registry в UAG

📌 Цель: хранение и разрешение capability contracts

📂 Файлы:

src/uag/registry/agent_capabilities.py


📋 Функции:

register_capability(agent_id, capability_contract)

resolve_capability(target_agent, capability)

validate_caller(agent_a, agent_b, capability)

📌 Capability Contract (YAML/JSON):

capability_name

allowed_callers

exposed_fields

constraints (опционально)

✅ DoD:

Capability доступна только разрешённым агентам

Попытка обхода → DENY

STEP 3 — UAG Routing для agent_query

📌 Цель: реализовать intent agent_query

📂 Файлы:

src/uag/sandbox/gateway.py
src/uag/core/access_controller.py


📋 Логика:

Валидировать intent = agent_query

Проверить capability existence

Проверить caller ∈ allowed_callers

Вызвать Fake Agent Provider

Отфильтровать response по exposed_fields

Залогировать решение

❌ Агент B никогда не фильтрует данные

✅ DoD:

Фильтрация работает строго по контракту

Любое нарушение → DENY

STEP 4 — AgentL0: поддержка agent_query

📌 Цель: агент умеет ТОЛЬКО вызывать intent

📂 Файлы:

src/agent/agent.py
src/agent/intent_dispatcher.py


📋 Добавить:

handle_intent("agent_query", payload)

📌 Важно:

agent.handle_intent() не знает, что это другой агент

агент не хранит адреса других агентов

агент не фильтрует ответ

✅ DoD:

AgentL0 вызывает UAG

AgentL0 корректно обрабатывает DENY

STEP 5 — Polygon L3 Scenarios

📌 Цель: реализовать сценарии из TEST_AGENT_INTERACTION_L3.md

📂 Файлы:

src/polygon/scenarios/pass_agent_to_agent_info.py
src/polygon/scenarios/fail_direct_agent_call.py
src/polygon/scenarios/fail_capability_escalation.py
src/polygon/scenarios/fail_deny_not_handled.py


📋 Сценарии тестируют:

только поведение

только через agent.handle_intent()

никакого доступа к internals

✅ DoD:

PASS/FAIL соответствуют TEST-документу

critical=True → SUSPENDED

STEP 6 — PolygonRunner L3

📌 Цель: запустить полный L3 workflow

📂 Файлы:

src/polygon/runner_l3.py
src/polygon/run_exam_l3.py


📋 Логика:

Preconditions: CERTIFIED_L2

IN_TRIAL → сценарии → verdict

PASS → CERTIFIED_L3

critical FAIL → SUSPENDED

✅ DoD:

python -m src.polygon.run_exam_l3


возвращает:

{ "verdict": "PASS", "lifecycle_state": "CERTIFIED_L3" }

4. Минимальный Demo-результат L3

После STEP 6 система умеет:

агент ↔ агент только через UAG

user-controlled access (capabilities)

data minimization

audit trail

enforcement через Polygon

🎯 Это реально продаваемый L3, а не концепт.

5. Что намеренно НЕ делаем в L3

Общую память между агентами

Делегацию прав

Multi-hop агентные цепочки

Самостоятельное управление доступом агентом

6. Статус документа

Document: IMPLEMENTATION_PLAN_L3.md

Level: L3

Status: APPROVED

Authority: Chief Architect / Project Owner

🧭 Твой следующий ход

Выбирай один:

1️⃣ Начинаем STEP 1 — Fake Agent Provider (код)
2️⃣ Хочешь — я сначала нарисую flow L3 (ASCII + sequence)
3️⃣ Или сразу минимальный код pass_agent_to_agent_info

Скажи номер — продолжаем.