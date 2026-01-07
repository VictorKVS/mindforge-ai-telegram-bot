# src/uag/intents.py

INTENTS = {
    # системные
    "who": "get_info",
    "ask": "llm_query",
    "plan": "llm_plan",
    "help": "get_help",

    # task manager
    "task_add": "task_create",
    "task_list": "task_read",
    "task_status": "task_read",
    "task_run": "task_execute",
    "task_run_all": "task_execute_bulk",

    # строительный домен
    "build_foundation": "build_foundation",

    # fallback
    "chat": "llm_chat"
}
