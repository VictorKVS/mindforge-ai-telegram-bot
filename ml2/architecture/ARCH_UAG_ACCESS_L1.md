ARCH_UAG_ACCESS_L1.md
Universal Agent Gateway — Access & Control Architecture (L1)
1. Назначение

UAG Access L1 определяет архитектурную модель допуска и контроля доступа для AI-агентов в экосистеме MindForge.

UAG является единственной точкой взаимодействия между агентами и любыми внешними ресурсами (провайдерами, сервисами, данными).

UAG — это не API-шлюз и не proxy.
UAG — это policy enforcement point для AI-агентов.

2. Архитектурная позиция
User / UI / Telegram
        ↓
     Agent L0
        ↓   (intent + context)
        ↓
       UAG
   (Access Control)
        ↓
    Providers / Services


UAG располагается строго между агентом и внешним миром.
Любой обход UAG считается архитектурным нарушением.

3. Ключевые архитектурные принципы (Инварианты)
3.1 Mandatory Gateway Rule

Агент НЕ имеет прямого доступа к:

API

Базам данных

Внешним сервисам

Любое действие агента проходит через UAG.

🔒 Нарушение → FAIL в Polygon → BLOCKED.

3.2 Intent-only Access

UAG принимает ТОЛЬКО intent-based запросы.

UAG НЕ принимает:

произвольные команды,

raw SQL,

HTTP-запросы от агента.

3.3 Zero Trust Agent Model

Агент считается недоверенным компонентом.

Агент:

не хранит секреты,

не знает ключей,

не принимает решений о правах.

UAG — единственный доверенный контроллер доступа.

4. Уровень L1: Ограничения и допущения

L1 — это минимально достаточный уровень безопасности, без усложнений.

Что есть в L1:

RBAC (role-based)

Intent allow/deny

Schema validation

Audit logging

Sandbox / Prod separation

Чего НЕТ в L1 (осознанно):

ABAC / policy language

Risk scoring

Contextual escalation

Adaptive policies

Learning policies

5. Access Control Model (L1)
5.1 Actors
Actor	Description
Agent	Источник intent
UAG	Контроллер доступа
Provider	Исполнитель действия
5.2 Access Decision Flow
Agent Intent
   ↓
UAG Validation
   ↓
RBAC Check
   ↓
Intent → Provider Mapping
   ↓
Provider Call
   ↓
Audit Log

6. RBAC Model (L1)
6.1 Роли (минимальный набор)
Role	Allowed
agent_l0	read-only intents (get_price, get_info)
agent_internal	расширенные intents (future)

RBAC жёстко статичен на L1.

6.2 Связь ролей и intents

intent ∈ role.allowed_intents

если intent не разрешён → DENY

7. Validation Layer

UAG обязан валидировать каждый запрос.

Проверки L1:

обязательные поля присутствуют

intent известен

schema соответствует контракту

target разрешён

❌ Любая ошибка → DENY.

8. DENY Semantics (L1)

DENY — это финальное решение.

При DENY:

действие не выполняется

provider не вызывается

агент получает отказ

событие логируется

UAG НЕ объясняет, почему отказано (L1).

9. Sandbox vs Production Separation
9.1 Принцип разделения

UAG-SANDBOX ≠ PROD-UAG

Разные:

registry providers

audit trails

RBAC policies

9.2 Context Marker

Каждый запрос содержит:

"context": {
  "env": "sandbox | prod",
  "source": "agent | polygon"
}


🔒 PROD-UAG отказывает запросам с env=sandbox.

10. Audit & Observability

UAG логирует каждое решение:

agent_id

intent

decision (ALLOW / DENY)

timestamp

env

Логи:

append-only

неизменяемые

используются Polygon и аудитом

11. Связь с Polygon

UAG НЕ знает о логике экзамена

UAG предоставляет:

audit logs

decision history

Polygon использует логи как доказательство

12. Failure Modes (L1)
Failure	Behavior
Unknown intent	DENY
Schema invalid	DENY
Provider missing	DENY
Sandbox/Prod mismatch	DENY

Принцип:
если сомневаешься — откажи.

13. Эволюция (не L1)
L2+ (не реализуем сейчас):

ABAC

Policy language

Contextual access

Dynamic risk scoring

Auto-suspension

L1-инварианты обязаны сохраниться.

14. Статус документа

Document: ARCH_UAG_ACCESS_L1.md

Status: PROPOSED

Level: L1

Authority: Chief Architect / Project Owner