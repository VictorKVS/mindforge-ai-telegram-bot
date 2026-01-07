# src/agent/profile/access_manager.py

import os
import json

# Путь к профилю — фиксированный, как в mindforge_ai_telegram_bot_shema_V_4.md
PROFILE_PATH = os.path.join(os.path.dirname(__file__), "profile.json")

# In-memory DB уровней доверия (для демо; в проде — Redis/SQLite)
_AGENT_LEVELS = {}

def get_access_level(agent_id: str) -> int:
    """Возвращает текущий уровень доверия агента (по умолчанию 0)"""
    return _AGENT_LEVELS.get(agent_id, 0)

def set_access_level(agent_id: str, level: int):
    """Устанавливает уровень доверия (0–6)"""
    if not (0 <= level <= 6):
        raise ValueError("Уровень доверия должен быть от 0 до 6")
    _AGENT_LEVELS[agent_id] = level

def increase_level(agent_id: str, new_level: int):
    """Повышает уровень, если новый выше текущего"""
    current = get_access_level(agent_id)
    if new_level > current:
        set_access_level(agent_id, new_level)

def get_profile_for_agent(agent_id: str) -> dict:
    """Возвращает видимую часть профиля для данного 