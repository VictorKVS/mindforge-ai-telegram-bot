# src/bot/handlers/security_filter.py

import re
import logging


class SecurityFilter:
    """
    Минимальная промышленная версия фильтра KM-6.
    Задача: отсеивать опасные сообщения, содержащие запросы
    на jailbreak, отключение фильтров, выполнение команд и т.п.
    """

    def __init__(self):
        # Базовый набор запрещённых шаблонов.
        # Можно расширять для KM-6 профиля.
        self.forbidden_patterns = [
            r"ignore all previous instructions",
            r"forget previous",
            r"please jailbreak",
            r"disable filter",
            r"отключи.*безопасность",
            r"system:",
            r"sudo rm -rf",
            r"cmd\.exe",
            r"powershell",
            r"eval\(",
            r"assert\(",
            r"execution",
            r"run this code",
            r"выполни команду",
            r"скажи что ты можешь нарушить",
        ]

        self.logger = logging.getLogger("SecurityFilter")

    # ----------------------------------------------------------
    # Основная проверка сообщения
    # ----------------------------------------------------------
    def check(self, text: str) -> bool:
        """
        Проверяет входящий текст на запрещённые паттерны.
        Возвращает True, если сообщение безопасно.
        """

        if not text:
            return True  # пустое сообщение безопасно

        # Нормализуем текст (безопасная практика)
        normalized = text.lower().strip()

        # Ищем запрещённые слова / паттерны
        for pattern in self.forbidden_patterns:
            if re.search(pattern, normalized, re.IGNORECASE):
                self.logger.warning(f"[SECURITY] Blocked message: {text}")
                return False

        return True
