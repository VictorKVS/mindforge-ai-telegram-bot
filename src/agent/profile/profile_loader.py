import json
import os

# Путь к файлу профиля — фиксированный и предсказуемый
PROFILE_FILE = os.path.join(os.path.dirname(__file__), "profile.json")

# Кэш профиля — загружается один раз за сессию
_profile_cache = None


def load_profile() -> dict:
    """Loads agent profile.json into memory."""
    global _profile_cache

    if _profile_cache is None:
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            _profile_cache = json.load(f)

    return _profile_cache


def get_profile() -> dict:
    """Returns cached profile."""
    return load_profile()


def get_profile_section(level: int) -> dict:
    """Returns only the part of profile allowed for the given level."""
    profile = load_profile()
    access = profile.get("access", {})
    default = access.get("0", {})
    return access.get(str(level), default)