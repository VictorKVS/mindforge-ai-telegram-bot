# src/bot/config.py
"""
File: G:\\agent-ecosystem-crkfl\\mindforge-ai-telegram-bot\\src\\bot\\config.py

Purpose:
Centralized configuration loader for MindForge Telegram Bot.

Responsibilities:
- Load configuration from .env
- Provide single settings object for the whole application
- Support runtime overrides (e.g. --demo mode)
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # -------------------------------------------------------------
    # TELEGRAM BOT
    # -------------------------------------------------------------
    TELEGRAM_TOKEN: str = ""

    # -------------------------------------------------------------
    # RUNTIME / ENVIRONMENT
    # -------------------------------------------------------------
    APP_ENV: str = "prod"                 # prod | demo
    DEFAULT_POLICY_MODE: str = "STRICT"   # STRICT | DEMO | OFF

    # -------------------------------------------------------------
    # LOCAL LLaMA CONFIG
    # -------------------------------------------------------------
    LOCAL_LLM_ENABLED: bool = False
    LOCAL_LLM_MODEL_PATH: str = "./models/llama/model.gguf"
    LOCAL_LLM_CTX: int = 4096
    LOCAL_LLM_THREADS: int = 6
    LOCAL_LLM_GPU_LAYERS: int = 0

    # -------------------------------------------------------------
    # API (RAG, UAG и прочие сервисы)
    # -------------------------------------------------------------
    KR_API_URL: str = "http://localhost:8000/rag/query"

    # -------------------------------------------------------------
    # LOGGING
    # -------------------------------------------------------------
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# -----------------------------------------------------------------
# Global singleton settings
# -----------------------------------------------------------------
settings = Settings()


def override_for_demo() -> None:
    """
    Runtime override for DEMO mode.

    This function is called when the application
    is started with the --demo flag.

    It DOES NOT modify .env.
    It ONLY affects in-memory configuration.
    """
    settings.APP_ENV = "demo"
    settings.DEFAULT_POLICY_MODE = "DEMO"

