import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, Union
import json
from enum import Enum

# Уровни логирования
class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Logger:
    """
    Универсальный логгер с поддержкой различных форматов и выводов.
    """
    
    def __init__(
        self,
        name: str = "app",
        log_level: LogLevel = LogLevel.INFO,
        log_to_file: bool = False,
        log_file_path: Optional[str] = None,
        log_format: Optional[str] = None,
    ):
        """
        Инициализация логгера.
        
        Args:
            name: Имя логгера
            log_level: Уровень логирования
            log_to_file: Записывать ли логи в файл
            log_file_path: Путь к файлу логов
            log_format: Формат строки лога
        """
        self.name = name
        self.log_level = log_level
        
        # Настройка формата по умолчанию
        if log_format is None:
            log_format = (
                "%(asctime)s - %(name)s - %(levelname)s - "
                "%(filename)s:%(lineno)d - %(message)s"
            )
        
        # Создание логгера
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level.value)
        
        # Удаление существующих обработчиков
        self.logger.handlers.clear()
        
        # Создание обработчика для консоли
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level.value)
        
        # Форматирование
        formatter = logging.Formatter(log_format)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # Обработчик для файла (если требуется)
        if log_to_file:
            if log_file_path is None:
                log_file_path = f"logs/{name}_{datetime.now().strftime('%Y%m%d')}.log"
            
            # Создание директории для логов
            log_path = Path(log_file_path)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
            file_handler.setLevel(log_level.value)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str, **kwargs):
        """Логирование на уровне DEBUG."""
        self._log_with_context(LogLevel.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Логирование на уровне INFO."""
        self._log_with_context(LogLevel.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Логирование на уровне WARNING."""
        self._log_with_context(LogLevel.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Логирование на уровне ERROR."""
        self._log_with_context(LogLevel.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Логирование на уровне CRITICAL."""
        self._log_with_context(LogLevel.CRITICAL, message, **kwargs)
    
    def _log_with_context(self, level: LogLevel, message: str, **kwargs):
        """Логирование с дополнительным контекстом."""
        if kwargs:
            context_str = " | " + " | ".join(f"{k}={v}" for k, v in kwargs.items())
            full_message = f"{message}{context_str}"
        else:
            full_message = message
        
        # Использование стандартного метода логирования
        log_method = getattr(self.logger, level.value.lower())
        log_method(full_message)
    
    def log_structured(self, event: str, data: Dict[str, Any], level: LogLevel = LogLevel.INFO):
        """
        Структурированное логирование в формате JSON.
        
        Args:
            event: Название события
            data: Данные события
            level: Уровень логирования
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "level": level.value,
            "logger": self.name,
            "data": data
        }
        
        log_message = json.dumps(log_entry, ensure_ascii=False)
        log_method = getattr(self.logger, level.value.lower())
        log_method(log_message)
    
    def log_exception(self, message: str, exc: Exception, **kwargs):
        """
        Логирование исключений с трассировкой.
        
        Args:
            message: Сообщение об ошибке
            exc: Объект исключения
        """
        self.error(f"{message}: {exc.__class__.__name__}: {str(exc)}", **kwargs)
        self.logger.exception(message)


# Функция для быстрого логирования (обратная совместимость)
def log(event: str, level: str = "INFO", **kwargs):
    """
    Простая функция логирования для тестов.
    
    Args:
        event: Событие для логирования
        level: Уровень логирования
        **kwargs: Дополнительные параметры контекста
    """
    logger = get_logger("simple")
    
    if kwargs:
        context_str = " | " + " | ".join(f"{k}={v}" for k, v in kwargs.items())
        event = f"{event}{context_str}"
    
    log_method = getattr(logger, level.lower())
    log_method(event)


# Глобальный экземпляр логгера по умолчанию
_default_logger = None

def get_logger(
    name: str = "app",
    level: LogLevel = LogLevel.INFO,
    log_to_file: bool = False
) -> Logger:
    """
    Фабрика для получения или создания логгера.
    
    Args:
        name: Имя логгера
        level: Уровень логирования
        log_to_file: Записывать ли логи в файл
        
    Returns:
        Экземпляр Logger
    """
    global _default_logger
    
    if name == "app" and _default_logger is not None:
        return _default_logger
    
    logger = Logger(name=name, log_level=level, log_to_file=log_to_file)
    
    if name == "app":
        _default_logger = logger
    
    return logger


# Декоратор для логирования вызовов функций
def log_function_call(logger: Optional[Logger] = None):
    """
    Декоратор для логирования входа и выхода из функции.
    
    Args:
        logger: Логгер для использования (если None, создается новый)
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Получаем или создаем логгер
            if logger is None:
                func_logger = get_logger(f"func.{func.__name__}")
            else:
                func_logger = logger
            
            # Логируем вход в функцию
            func_logger.info(
                f"Calling {func.__name__}",
                args=str(args),
                kwargs=str(kwargs)
            )
            
            try:
                # Выполняем функцию
                result = func(*args, **kwargs)
                
                # Логируем успешный выход
                func_logger.info(
                    f"Function {func.__name__} completed successfully"
                )
                
                return result
            except Exception as e:
                # Логируем ошибку
                func_logger.error(
                    f"Function {func.__name__} failed",
                    error=str(e)
                )
                raise
        
        return wrapper
    return decorator


# Инициализация логгера по умолчанию при импорте
default_logger = get_logger("app", LogLevel.INFO)

# Пример использования
if __name__ == "__main__":
    # Простое логирование
    log("Тестовое событие", user_id=123, action="login")
    
    # Использование класса Logger
    logger = Logger("test", LogLevel.DEBUG, log_to_file=True)
    logger.info("Запуск приложения", version="1.0.0")
    logger.debug("Отладочная информация", data={"test": True})
    logger.warning("Предупреждение", issue="low_memory")
    
    try:
        raise ValueError("Тестовая ошибка")
    except ValueError as e:
        logger.log_exception("Ошибка выполнения", e, context="test")
    
    # Структурированное логирование
    logger.log_structured(
        "user_registered",
        {"user_id": 456, "email": "test@example.com"},
        LogLevel.INFO
    )
    
    # Использование декоратора
    @log_function_call()
    def example_function(x, y):
        return x + y
    
    result = example_function(5, 3)
    print(f"Result: {result}")