mindforge-ai-telegram-bot/
│
├── src/
│   ├── bot/
│   │   ├── ai/
│   │   │   ├── llm_client.py
│   │   │   ├── llm_router.py
│   │   │   ├── task_engine.py      ← ГОТОВ
│   │   │
│   │   ├── handlers/
│   │   │   ├── model_handler.py   ← ДОБАВЛЕН ДЕТЕКТОР ФУНДАМЕНТА
│   │   │   ├── build_handler.py   ← СДЕЛАЕМ ЗАВТРА (FSM)
│   │   │
│   │   ├── uag/
│   │   │   ├── rozetka_service.py ← НУЖНО ДОБАВИТЬ ЗАВТРА
│   │   │   ├── stores_db.json     ← ПРАЙСЫ МАГАЗИНОВ
│   │   │
│   │   ├── bot.py                 ← запускается вручную
│   │
│   ├── uag_core/                  ← ML2 ядро (gateway, drivers)
│   │   ├── gateway.py
│   │   ├── router.py
│   │   ├── normalizer.py
│   │   ├── drivers/
│   │   │   ├── market_driver.py   ← ВСТАВИМ КАК МАГАЗИННЫЙ ДРАЙВЕР
│   │   │   ├── sql_driver.py
│   │   │   ├── ticket_driver.py
│   │   ├── contracts/
│   │   │   ├── ROUTER_CONTRACT.md
│   │   │   ├── GATEWAY_CONTRACT.md
│   │   │   ├── DRIVERS_CONTRACT.md
│   │   │   ├── SECURITY_CONTRACT.md
│   │   │
│   │   ├── tests/
│   │   │   ├── test_market_driver.py
│   │   │   ├── test_gateway.py
│   │   │   ├── test_router.py
│
├── models/
├── tasks.json
└── README.md
