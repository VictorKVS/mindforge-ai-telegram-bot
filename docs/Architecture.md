# MindForge AI Telegram Bot — Architecture Blueprint

This architecture is synchronized with the file:

**mindforge_ai_telegram_bot_shema.md**

The repository structure, modules, and integrations must always match this blueprint.

> ⚠️ Any change in the project must be reflected in the schema file.

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
├── docs/
│   ├── Architecture.md
│   ├── Features.md
│   └── Security.md
│
├── src/
│   ├── bot.py
│   ├── config.py
│   ├── ai/
│   │   ├── llm_client.py
│   │   └── rag_engine.py
│   ├── handlers/
│   │   ├── base.py
│   │   └── security_filter.py
│   └── utils/
│       ├── logger.py
│       └── validators.py
│
└── tests/
    ├── test_handlers.py
    ├── test_llm.py