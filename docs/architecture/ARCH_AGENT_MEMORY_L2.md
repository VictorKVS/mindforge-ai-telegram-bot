ARCH_AGENT_MEMORY_L2.md
MindForge · Agent Memory Architecture (L2)
1. Purpose / Назначение

Agent Memory L2 вводит управляемую память агента для повышения полезности и устойчивости поведения без нарушения Zero Trust и Mandatory Gateway Rule.

Память предназначена для:

хранения контекста взаимодействий,

поддержки многократных шагов и сценариев,

аккуратного использования прошлого опыта в пределах политик.

Ключевое разграничение

Memory ≠ Knowledge Base

Memory ≠ Logs

Компонент	Роль
Memory	Контекст и состояние агента
Knowledge Base	Факты и документы
Logs	Доказательство поведения

Память не является источником знаний и не используется для принятия решений о доступе.

2. Architectural Position
User / UI / Telegram
        ↓
     Agent
        ↓ (intent: memory_read / memory_write)
        ↓
       UAG
 (policy enforcement)
        ↓
   Memory Provider


Любой доступ к памяти осуществляется только через UAG.
Прямой доступ агента к хранилищу памяти запрещён.

3. Core Principles (Invariants)

Memory is a Provider
Память — provider, аналогичный KB и shop.

Intent-only Memory Access
Только разрешённые intents.

Policy-bound Memory
Политики доступа определяются в UAG.

Audit-first
Все операции чтения/записи логируются.

Non-decision-making
Память не принимает решений и не влияет на права.

4. Memory Types (L2)
4.1 Short-term Memory

контекст текущей сессии,

временные ключи/значения,

TTL-очистка.

Назначение: поддержка диалога и пошаговых сценариев.

4.2 Long-term Memory

внешнее хранилище (SQL / KV / Vector),

доступ только по intent,

versioned records.

Назначение: накопление контекста в рамках разрешённой области.

4.3 Policy-bound Memory

память с жёсткими scope’ами,

раздельные пространства (agent_scope, user_scope),

строгие лимиты записи.

Назначение: предотвращение «утечки контекста».

5. Access Model
5.1 Memory Intents (conceptual)
{
  "agent_id": "agent_l0",
  "intent": "memory_read",
  "memory_scope": "session",
  "key": "current_order_context",
  "context": { "env": "prod" }
}

{
  "agent_id": "agent_l0",
  "intent": "memory_write",
  "memory_scope": "session",
  "key": "current_order_context",
  "value": { "step": "price_received" },
  "context": { "env": "prod" }
}

5.2 Enforcement (UAG)

UAG:

валидирует схему,

проверяет RBAC/ABAC (L2-ready),

ограничивает scope,

применяет rate limits,

логирует операции.

6. What Memory Does NOT Store (Critical)

Память не должна содержать:

персональные данные (PII),

секреты и ключи,

reasoning / chain-of-thought,

сырые пользовательские тексты (в prod),

знания, доступные через KB.

7. Interaction with KB & Logs

Memory может хранить ссылки на KB-источники (IDs, URIs),

Memory не дублирует знания,

Logs фиксируют факт доступа, а не содержимое.

8. Interaction with Polygon

Polygon проверяет, что агент:

использует memory только через UAG,

не пишет в запрещённые scope’ы,

корректно обрабатывает DENY при доступе к памяти,

не использует память для обхода политик.

Нарушение → FAIL / SUSPENDED (L2).

9. Security & Compliance

Принципы:

Memory is constrained

No silent persistence

Explicit write permissions

Full auditability

Least privilege by default

10. Deployment & Isolation (L2)

Начальная реализация:

fake_memory_provider,

sandbox-only,

без prod-данных.

Переход в prod:

только после L2 сертификации,

с включённым мониторингом.

11. Explicit Decisions Requiring Approval

Набор memory intents

memory_read

memory_write

memory_clear

Scopes памяти

session

agent

user (опционально, L2+)

Хранилище

внешний provider (рекомендовано)

не встроенное в Agent

12. Related Documents

ARCH_AGENT_L0.md

ARCH_UAG_ACCESS_L1.md

ARCH_LOGGING_L2.md

ARCH_KNOWLEDGE_BASE_L2.md

PROCESS_RECERTIFICATION_L2.md (планируется)

13. Document Status
Document: ARCH_AGENT_MEMORY_L2.md
Level: L2
Status: PROPOSED
Authority: Chief Architect / Project Owner

Итоговая формула

Agent думает.
UAG решает.
Memory помнит (по правилам).
KB знает.
Logs доказывают.
Polygon проверяет.

🔒 END OF DOCUMENT