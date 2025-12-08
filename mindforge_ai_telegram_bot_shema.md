mindforge-ai-telegram-bot/
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── security.yml
│
├── tools/
│   └── plantuml.jar                     # Для генерации диаграмм из .puml
│
├── docs/
│   ├── agents/
│   │   ├── interview_agent_spec.md      # Спецификация: входы, выходы, алгоритм
│   │   ├── interview_agent_testplan.md  # План тестирования (unit, integration)
│   │   ├── interview_agent_architecture.md # (опционально) внутреннее устройство
│   │   └── uml/
│   │       ├── interview_agent_flow.puml     # Диаграмма состояний/решений
│   │       └── interview_agent_sequence.puml # Взаимодействие: бот → агент → RAG → LLM
│   │
│   ├── architecture.md                  # Обзор всей системы
│   ├── security.md                      # Защита от prompt injection, аудит
│   ├── rag.md                           # Работа с базой знаний
│   ├── api.md                           # Описание /rag/query и других эндпоинтов
│   └── images/
│       ├── neon_banner.png
│       └── schema.png
│
├── src/
│   ├── api/                             # Локальный REST API (для интеграций)
│   │   ├── main.py
│   │   └── routes/
│   │       └── rag.py                   # POST /rag/query
│   │
│   ├── bot/
│   │   ├── bot.py                       # Основной Telegram-движок
│   │   ├── config.py
│   │   ├── handlers/
│   │   │   ├── base.py
│   │   │   ├── security_filter.py
│   │   │   └── interview_handler.py     # Обработка команды /interview
│   │   ├── ai/
│   │   │   ├── llm_client.py            # Работа с Llama/OpenAI
│   │   │   ├── rag_engine.py            # ← вызывает localhost:8000/rag/query
│   │   │   ├── agent_orchestrator.py    # ← KM-6: управление жизненным циклом агентов
│   │   │   └── agents/
│   │   │       └── interview_agent.py   # ← Основная логика интервьюера
│   │   └── utils/
│   │       ├── logger.py
│   │       └── validators.py
│   │
│   └── shared/                          # Общие утилиты
│       ├── security/
│       └── config_loader.py
│
└── tests/
    ├── agents/
    │   ├── test_interview_agent.py      # Юнит-тесты логики оценки
    │   └── test_interview_flow.py       # Интеграционные сценарии
    ├── bot/
    │   ├── test_handlers.py
    │   ├── test_llm.py
    │   └── test_security.py
    ├── api/
    │   └── test_rag_endpoint.py
    └── shared/