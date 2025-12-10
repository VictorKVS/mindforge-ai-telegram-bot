import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # -------------------------------------------------------------
    # TELEGRAM BOT
    # -------------------------------------------------------------
    TELEGRAM_TOKEN: str = ""

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


# Глобальный синглтон настроек
settings = Settings()
