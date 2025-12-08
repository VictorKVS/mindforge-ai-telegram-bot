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
│   ├── index.md
│   ├── architecture.md
│   ├── security.md
│   ├── rag.md
│   ├── api.md
│   ├── features.md
│   │
│   ├── llm_router/                     # ← НОВОЕ
│   │   ├── llm_router_spec.md
│   │   ├── llm_router_architecture.md
│   │   ├── llm_router_audit.md
│   │   └── llm_router_future_work.md
│   │
│   ├── agents/                         # ← НОВОЕ
│   │   ├── interview_agent_spec.md
│   │   ├── interview_agent_testplan.md
│   │   └── interview_agent_architecture.md
│   │
│   ├── uml/
│   │   ├── architecture.puml
│   │   ├── sequence.puml
│   │   ├── llm_router_sequence.puml        # ← НОВОЕ
│   │   ├── llm_router_components.puml      # ← НОВОЕ
│   │   └── llm_router_fallback_activity.puml
│   │
│   └── images/
│       ├── neon_banner.png
│       └── schema.png
│
├── src/
│   ├── api/
│   │   ├── main.py
│   │   └── routes/
│   │       └── rag.py
│   │
│   └── bot/
│       ├── bot.py
│       ├── config.py
│       │
│       ├── ai/
│       │   ├── llm_router.py                # v2.1
│       │   ├── rag_engine.py
│       │   ├── llm_client.py                # общий слой LLM
│       │   │
│       │   └── agents/                      # ← НОВОЕ
│       │       └── interview_agent.py
│       │
│       ├── handlers/
│       │   ├── base.py
│       │   ├── security_filter.py
│       │   ├── model_handler.py             # ← НОВОЕ
│       │   └── interview_handler.py
│       │
│       ├── km6/                             # ← НОВОЕ
│       │   ├── safety_contract.yaml
│       │   ├── policy_engine.py
│       │   └── orchestrator.py
│       │
│       └── utils/
│           ├── logger.py
│           └── validators.py
│
├── shared/
│   ├── security/
│   │   ├── masking.py
│   │   ├── audit.py
│   │   └── permissions.py
│   └── config_loader.py
│
├── tests/
│   ├── llm/                               # ← НОВОЕ
│   │   ├── test_llm_router_basic.py
│   │   ├── test_llm_router_fallback.py
│   │   ├── test_llm_router_context_manager.py
│   │   ├── test_llm_router_cache.py
│   │   ├── test_llm_router_metrics.py
│   │   ├── test_llm_router_health.py
│   │   ├── test_llm_router_rate_limit.py
│   │   └── test_llm_router_async.py
│   │
│   ├── api/
│   ├── bot/
│   └── shared/
│
└── tools/
    └── plantuml.jar
