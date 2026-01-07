ADR → Roadmap → Backlog
Traceability Map (Architecture → Execution)
🎯 Назначение документа

Этот документ связывает:

архитектурные решения (ADR)

этапы зрелости (Roadmap: L1 → L2 → L3)

конкретные задачи реализации (Backlog / Epics / Tasks)

Ключевой принцип:

Ни одной задачи без архитектурного основания.
Ни одного ADR без реализации.

1️⃣ Общая схема связи
ADR (WHY / WHAT)
   ↓
Roadmap Level (WHEN)
   ↓
Epic (AREA)
   ↓
Task (HOW)

2️⃣ Карта ADR → Roadmap Levels
ADR	Название	L1	L2	L3
ADR-0001	AISOC Core	⚠️ partial	✅ core	🔁 extend
ADR-0002	Policy & Trust Model	❌	✅	🔁 adaptive
ADR-0003	Agent Lifecycle & Governance	⚠️ basic	✅	🔁 scale
ADR-0004	Audit & Explainability	⚠️ logs	✅	🔁 analytics
ADR-0005	Risk Scoring & Runtime	❌	⚠️ rules	✅
ADR-0006	Connector Security & Data Access	⚠️ safe	✅	🔁 dynamic
ADR-0007	Compliance & Regional Zoning	❌	⚠️ config	✅

Легенда:

❌ — не реализуется

⚠️ — частично / stub

✅ — обязательно

🔁 — развитие

3️⃣ L1 → Backlog (Controlled MVP)
🎯 Цель L1

Рабочий демо / пилот без прямого доступа и без ИБ-рисков

Epic L1-01: Scenario-driven UAG

ADR: 0001, 0003

Tasks:

 Выделить Agent как intent-only

 Вынести сценарии из Telegram-bot логики

 Реализовать UAG gateway (stub)

 Запретить прямые side-effects из агента

Epic L1-02: Memory Safety

ADR: 0006

Tasks:

 Ввести memory_adapter

 Ограничить память scope (session-only)

 Запретить raw read/write

 Санитизация данных

Epic L1-03: Minimal Audit

ADR: 0004

Tasks:

 Логирование intent → action

 Связь события с agent_id

 Хранение логов (stdout / file)

4️⃣ L2 → Backlog (AISOC Core)
🎯 Цель L2

Минимально допустимый production-уровень

Epic L2-01: AISOC Core

ADR: 0001

Tasks:

 Decision API (ALLOW / DENY / CONFIRM)

 Enforcement point до действия

 Kill-switch агента

 Централизация принятия решений

Epic L2-02: Policy & Trust Engine

ADR: 0002

Tasks:

 Модель trust levels

 Declarative policy (YAML/JSON)

 Policy evaluation pipeline

 Связь policy ↔ agent ↔ action

Epic L2-03: Audit & Explainability

ADR: 0004

Tasks:

 Structured audit events

 Причина решения (why DENY)

 Correlation ID для цепочек

 API получения истории решений

Epic L2-04: Risk Scoring (Rule-based)

ADR: 0005

Tasks:

 Базовая модель риска

 Пороговые значения

 Эскалация CONFIRM

 Логирование risk events

Epic L2-05: Secure Connectors

ADR: 0006

Tasks:

 Read-only коннектор

 Mapping action → connector

 Data masking / filtering

 Запрет произвольных запросов

5️⃣ L3 → Backlog (Adaptive & Scale)
🎯 Цель L3

Снижение ручного контроля и рост масштаба

Epic L3-01: Adaptive Risk Engine

ADR: 0005

Tasks:

 Поведенческий анализ

 Динамические risk thresholds

 Контекстные реакции

Epic L3-02: Threat Intelligence

ADR: 0001, 0005

Tasks:

 Каталог паттернов атак

 Jailbreak / prompt injection detection

 Автообновление сигнатур

Epic L3-03: Compliance Automation

ADR: 0007

Tasks:

 Региональные policy profiles

 Compliance checks

 Evidence export (audit packs)

6️⃣ Как этим пользоваться (важно)
Для разработки

Любая задача → должна ссылаться на Epic → ADR

Нет ADR → нет задачи

Для Раниса / бизнеса

Видно, за что платят

Понятно, что входит в этап

Нет «вдруг выросло»

Для ИБ / аудиторов

Видна трассируемость

Понятно, где контроль

Можно проверять этапами

7️⃣ Куда положить в проекте

Рекомендовано:

docs/
 ├── ADR/
 ├── Roadmap.md
 ├── ADR_TO_BACKLOG.md   ← ЭТОТ ДОК
 └── architecture/

Итог (одной строкой)

ADR объясняет ПОЧЕМУ.
Roadmap — КОГДА.
Backlog — КАК.

Готов продолжать:

разложить L1 или L2 в конкретные Sprint’ы

выбрать 1 Epic и разрезать в код

помочь оформить это в GitHub Issues / Projects

Скажи, что берём первым.