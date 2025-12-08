# LLMRouter — Component Specification
Version: 2.1  
Author: MindForge AI Architecture Team  
Date: 2025-12-08  

---

## 1. Purpose

LLMRouter обеспечивает универсальный, отказоустойчивый и управляемый слой вызовов LLM-моделей.

Компонент используется в:
- InterviewAgent  
- RAG Engine  
- KM-6 Orchestrator  
- UAG Policy Engine  
- Telegram Bot  

---

## 2. Responsibilities

### Router отвечает за:
- выбор LLM-провайдера  
- fallback при ошибках  
- кэширование  
- сбор метрик  
- контроль скорости (rate limit)  
- health-check  
- переключение провайдера по контексту  
- асинхронную интеграцию  

---

## 3. Supported Providers

| Provider | Description | Region |
|---------|-------------|--------|
| OpenAI | GPT-3.5/4 | International |
| GigaChat | SberCloud | Russia |
| LLaMA / Ollama | Local model | Local |
| Qwen | Alibaba | International |
| DeepSeek | DeepSeek AI | International |

---

## 4. Public API

### `ask(prompt: str, provider: Optional[str]) -> str`
Синхронный вызов модели.

### `ask_async(prompt: str, provider: Optional[str]) -> Awaitable[str>`
Асинхронная версия.

### `list_providers() -> List[str]`
Получить список всех моделей.

### `set_default(provider: str)`
Установить модель по умолчанию.

### `temporary_provider(provider: str)`
Временное переключение модели в контексте.

### `health_check() -> Dict`
Состояние всех моделей.

### `get_metrics(reset=False) -> Dict`
Метрики работы роутера.

---

## 5. Configuration (Pydantic)

### Model:
```python
class LLMRouterConfig(BaseSettings):
    default_provider: str = "llama"
    fallback_order: List[str]
    cache_size: int
    log_level: str
Настройки задаются через ENV переменные:

makefile
Копировать код
LLM_ROUTER_DEFAULT_PROVIDER=
LLM_ROUTER_FALLBACK_ORDER=
LLM_ROUTER_CACHE_SIZE=
LLM_ROUTER_LOG_LEVEL=
6. Behavior Requirements
Fallback
Router должен пытаться обращаться к моделям в указанном приоритете fallback:

css
Копировать код
[ requested → openai → gigachat → llama → qwen → deepseek ]
Rate Limit
Если лимит превышен:
RuntimeError("Rate limit exceeded")

Metrics
Router должен сохранять:

total_requests

error_count

latency_log

7. Error Handling
Все ошибки сборются в словарь:

json
Копировать код
{ "provider_name": "error_message" }
и возвращаются в исключении:

css
Копировать код
RuntimeError("All LLM providers failed. Errors: {...}")
8. Non-functional Requirements
Performance
avg latency <= 1.0 sec (cache warm)

Security
no direct internet access bypass

all outbound calls controlled by UAG

Reliability
99.9% uptime при наличии fallback моделей

9. Dependencies
Pydantic BaseSettings

logging

asyncio

collections.deque

yaml
Копировать код

---

# 📁 **2.2. llm_router_architecture.md — Архитектурный документ**

Файл:
docs/llm_router/llm_router_architecture.md

yaml
Копировать код

```markdown
# LLMRouter Architecture
Version: 2.1  
MindForge KM-6 Platform  

---

## 1. High-Level Architecture

Caller → LLMRouter → ProviderSelector → RateLimiter → Cache → LLM Client → Response

yaml
Копировать код

---

## 2. Component Diagram

*(см. UML–файл)*

---

## 3. Fallback Workflow

1. Receive prompt  
2. Validate provider  
3. Check rate limit  
4. Build fallback chain  
5. Try provider N  
6. If success → return  
7. Else → log error → next provider  
8. Если все упали → RuntimeError  

---

## 4. Internal Subsystems

### 4.1 ProviderManager
- хранит словарь всех моделей  
- отвечает за provider switching  

### 4.2 RateLimiter
- sliding window на deque  
- предотвращает превышение SLA  

### 4.3 CacheManager
- LRU cache  
- хэш-ключ prompt  

### 4.4 MetricsSubsystem
- latency  
- errors  
- success rate  

### 4.5 AsyncEngine
- обеспечивает ask_async  

---

## 5. Data Flow Diagram (DFD Level 1)

User → Bot → UAG → LLMRouter → Provider → Response

yaml
Копировать код

---

## 6. Extensibility

LLMRouter поддерживает:

- добавление новых моделей  
- добавление новых стратегий fallback  
- расширенные алгоритмы выбора модели (ML)  
- маршрутизацию по политике UAG  

---

## 7. Threat Model (MST / STRIDE)

| Threat | Mitigation |
|--------|------------|
| DoS через частые запросы | Rate limit |
| Prompt Injection | UAG sanitization |
| Compromised provider | Fallback |
| Data Exfiltration | Политика соотв. данных (152-ФЗ, GDPR) |
| Latency spike | Metrics, health-check |

---

## 8. Integration Points

LLMRouter используется в:

- RAG Engine  
- InterviewAgent  
- Telegram Bot  
- KM-6 Orchestrator  
- UAG Policy Engine  

---
