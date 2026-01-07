# src/bot/config.py
"""
File: G:\\agent-ecosystem-crkfl\\mindforge-ai-telegram-bot\\src\\bot\\config.py

Purpose:
Centralized configuration loader for MindForge Telegram Bot.

Responsibilities:
- Load configuration from .env
- Provide a single settings object for the whole application
- Support runtime overrides (e.g. --demo mode)
- Act as the single source of truth for runtime configuration
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # -------------------------------------------------------------
    # TELEGRAM BOT
    # -------------------------------------------------------------
    TELEGRAM_TOKEN: str = ""
    AGENT_NAME: str = "MindForge-Demo-Agent"

    #  -------------------------------------------------------------
    # APPLICATION / BRANDING
    # -------------------------------------------------------------
    APP_VERSION: str = "0.0.0"
    BRAND_PROFILE: str = "default"   # default | partner_x | demo | etc


    # -------------------------------------------------------------
    # RUNTIME / ENVIRONMENT
    # -------------------------------------------------------------
    APP_ENV: str = "prod"                 # prod | demo
    DEFAULT_POLICY_MODE: str = "STRICT"   # STRICT | DEMO | OFF

    # -------------------------------------------------------------
    # LOCAL LLaMA CONFIG (future use)
    # -------------------------------------------------------------
    LOCAL_LLM_ENABLED: bool = False
    LOCAL_LLM_MODEL_PATH: str = "./models/llama/model.gguf"
    LOCAL_LLM_CTX: int = 4096
    LOCAL_LLM_THREADS: int = 6
    LOCAL_LLM_GPU_LAYERS: int = 0

    # -------------------------------------------------------------
    # API (RAG / UAG / external services)
    # -------------------------------------------------------------
    KR_API_URL: str = "http://localhost:8000/rag/query"

    # -------------------------------------------------------------
    # LOGGING
    # -------------------------------------------------------------
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    # -------------------------------------------------------------
    # FEATURE FLAGS (UI / DEMO / PRODUCT)
    # -------------------------------------------------------------
    FEATURE_AUDIT_PANEL: bool = True
    FEATURE_STATUS_PANEL: bool = True
    FEATURE_AGENT_CONTROL: bool = True



# -----------------------------------------------------------------
# Global singleton settings
# -----------------------------------------------------------------
settings = Settings()


def override_for_demo() -> None:
    """
    Runtime override for DEMO mode.

    This function is called when the application
    is started with the --demo flag.

    IMPORTANT:
    - Does NOT modify .env
    - Only mutates the in-memory settings object
    """

    settings.APP_ENV = "demo"
    settings.DEFAULT_POLICY_MODE = "DEMO"
