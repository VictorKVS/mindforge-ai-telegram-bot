IMPLEMENTATION_PLAN_L2.md
📍 Путь в проекте:

docs/IMPLEMENTATION_PLAN_L2.md


Ниже — финальный, рабочий план реализации L2, который можно сразу класть в репозиторий. Это не абстракция, а чек-лист для кодинга без хаоса.

📄 IMPLEMENTATION_PLAN_L2.md
MindForge · L2 Implementation Execution Plan
1. Purpose / Назначение

Данный документ определяет пошаговый план реализации уровня L2 экосистемы MindForge.

Цель плана:

материализовать утверждённые ARCH / CONTRACT / TEST / PROCESS документы,

исключить архитектурные отклонения в коде,

обеспечить воспроизводимую реализацию с чёткими критериями готовности (DoD),

подготовить систему к L2 сертификации в Polygon.

2. Implementation Principles (Mandatory)

Contracts-first
Код реализует контракты, а не наоборот.

No business logic in providers
Providers (Memory, KB) не принимают решений — только исполняют.

UAG as single enforcement point
Вся логика доступа — в UAG.

Sandbox-only until L2 PASS
Никакого prod-кода до сертификации.

Fail fast, audit always
Любая ошибка — DENY + audit.

3. High-Level Execution Order (L2)

Реализация выполняется строго в следующем порядке:

Fake Memory Provider

Fake Knowledge Base Provider

Интеграция Providers в UAG-SANDBOX

Расширение Polygon Runner для L2

Прогон TEST_L2_INTEGRATION_CURRICULUM

Фиксация L2 PASS (tag / docs)

4. Step-by-Step Implementation Plan
🔹 STEP 1 — Fake Memory Provider

📍 Файлы:

src/providers/fake_memory_provider.py


📌 Реализует контракты:

CONTRACT_MEMORY_ACCESS_L2.md

📋 Минимальный API:

read(agent_id, scope, key)

write(agent_id, scope, key, value)

clear(agent_id, scope, key)

📦 Хранилище:

In-memory dict

Key format: {agent_id}:{scope}:{key}

🔐 Ограничения:

sandbox-only

без логирования value

без persistence

✅ DoD (Definition of Done):

memory_read возвращает OK/null по контракту

memory_write валидирует scope и intent

memory_clear не допускает mass-delete

все операции формируют audit events

🔹 STEP 2 — Fake Knowledge Base Provider

📍 Файлы:

src/providers/fake_kb_provider.py


📌 Реализует контракты:

CONTRACT_KB_ACCESS_L2.md

📋 Минимальный API:

query(scope, query)

retrieve(scope, document_id)

📦 Данные:

Статический набор документов (dict / json)

🔐 Ограничения:

read-only

sandbox-only

без интерпретаций

без state

✅ DoD:

knowledge_query возвращает массив документов

document_retrieve возвращает 1 документ или пусто

поля строго по контракту

audit events формируются

🔹 STEP 3 — Интеграция Providers в UAG-SANDBOX

📍 Файлы:

src/uag/sandbox/provider_registry.py
src/uag/sandbox/gateway.py


📌 Изменения:

регистрация fake_memory_provider

регистрация fake_kb_provider

intent routing:

memory_* → memory provider

knowledge_* → KB provider

🔐 Контроль:

schema validation

RBAC

scope enforcement

rate limits (заглушка допустима)

✅ DoD:

прямой доступ к providers невозможен

любой доступ идёт через UAG

DENY корректно возвращается агенту

🔹 STEP 4 — Polygon Runner (L2)

📍 Файлы:

src/polygon/runner.py
src/polygon/scenarios/


📌 Изменения:

поддержка L2 lifecycle

исполнение:

TEST_MEMORY_ACCESS_L2

TEST_KB_ACCESS_L2

TEST_L2_INTEGRATION_CURRICULUM

🔁 Fail-fast:

первый FAIL → остановка

📄 Выход:

verdict.json

certification_history_id

✅ DoD:

корректные переходы lifecycle

SUSPENDED при критических нарушениях

артефакты сохраняются

🔹 STEP 5 — Test Execution

📍 Тесты:

docs/specs/ml2/tests/TEST_MEMORY_ACCESS_L2.md
docs/specs/ml2/tests/TEST_KB_ACCESS_L2.md
docs/specs/ml2/tests/TEST_L2_INTEGRATION_CURRICULUM.md


📌 Порядок:

Memory tests

KB tests

Integration tests

✅ DoD:

все mandatory scenarios PASS

audit trail полный

verdict = PASS

🔹 STEP 6 — L2 Finalization

📍 Git:

git commit -m "L2: certified (memory + kb + integration)"
git tag L2-CERTIFIED
git push --tags


📄 Docs update:

README

ARCH_DEV_JOURNAL.md

✅ DoD:

L2 статус зафиксирован

готовность к L2.5 Monitoring

5. Explicit Non-Goals (L2)

❌ Реализация prod memory
❌ Реализация prod KB
❌ Оптимизация производительности
❌ ML training
❌ UI / Telegram изменения

6. Success Criteria (L2)

L2 считается завершённым, если:

агент получает CERTIFIED_L2,

все сценарии Polygon PASS,

Memory и KB работают только через UAG,

нет архитектурных отклонений.

7. Status
Document: IMPLEMENTATION_PLAN_L2.md
Status: APPROVED
Level: L2
Authority: Chief Architect / Project Owner

🔒 Итоговая формула реализации

No code without contract.
No access without UAG.
No power without certification.

END OF DOCUMENT

