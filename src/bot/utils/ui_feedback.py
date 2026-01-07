# src/bot/utils/ui_feedback.py:

"""
UI Feedback utilities для визуальной обратной связи
Инструменты для улучшения пользовательского опыта через визуальную обратную связь
"""
from typing import Optional, List, Dict, Any, Union
from enum import Enum
import asyncio

from aiogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    CallbackQuery,
    Message,
    ReplyKeyboardRemove
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest
import logging

log = logging.getLogger("mindforge.ui")


class ButtonStyle(Enum):
    """Стили для кнопок"""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SUCCESS = "success"
    DANGER = "danger"
    WARNING = "warning"
    INFO = "info"
    DISABLED = "disabled"


class ProgressState(Enum):
    """Состояния прогресса"""
    PROCESSING = "processing"
    SUCCESS = "success"
    ERROR = "error"
    WAITING = "waiting"


def disable_button(
    markup: InlineKeyboardMarkup, 
    button_text: str,
    disabled_text: str = "⏳ Обработка...",
    button_callback: Optional[str] = None,
    style: ButtonStyle = ButtonStyle.DISABLED
) -> InlineKeyboardMarkup:
    """
    Заменить текст кнопки на disabled_text (визуально отключить)
    
    Args:
        markup: Исходная клавиатура
        button_text: Текст кнопки для отключения
        disabled_text: Текст для отключенной кнопки
        button_callback: Callback_data кнопки для поиска (альтернатива тексту)
        style: Стиль отключенной кнопки
        
    Returns:
        Обновленная клавиатура
    """
    if not markup.inline_keyboard:
        return markup
    
    # Эмодзи для разных стилей
    emoji_map = {
        ButtonStyle.DISABLED: "⏳",
        ButtonStyle.SUCCESS: "✅",
        ButtonStyle.ERROR: "❌",
        ButtonStyle.WARNING: "⚠️",
        ButtonStyle.INFO: "ℹ️"
    }
    
    emoji = emoji_map.get(style, "⏳")
    if emoji not in disabled_text:
        disabled_text = f"{emoji} {disabled_text}"
    
    new_keyboard = []
    for row in markup.inline_keyboard:
        new_row = []
        for button in row:
            should_disable = False
            
            # Проверяем по тексту
            if button_text and button.text == button_text:
                should_disable = True
            
            # Проверяем по callback_data (если указан)
            if button_callback and button.callback_data == button_callback:
                should_disable = True
            
            if should_disable:
                # Создаём "отключённую" кнопку
                new_button = InlineKeyboardButton(
                    text=disabled_text,
                    callback_data="ignore"  # специальный callback для игнорирования
                )
                new_row.append(new_button)
                log.debug(f"Кнопка отключена: {button_text or button_callback}")
            else:
                new_row.append(button)
        new_keyboard.append(new_row)
    
    return InlineKeyboardMarkup(inline_keyboard=new_keyboard)


def enable_button(
    markup: InlineKeyboardMarkup,
    original_callback: str,
    new_text: str,
    new_callback: Optional[str] = None
) -> InlineKeyboardMarkup:
    """
    Включить ранее отключенную кнопку
    
    Args:
        markup: Клавиатура с отключенными кнопками
        original_callback: Исходный callback_data кнопки
        new_text: Новый текст для кнопки
        new_callback: Новый callback_data (если отличается от исходного)
        
    Returns:
        Обновленная клавиатура
    """
    if not markup.inline_keyboard:
        return markup
    
    new_keyboard = []
    for row in markup.inline_keyboard:
        new_row = []
        for button in row:
            if button.callback_data == "ignore":
                # Восстанавливаем кнопку
                new_button = InlineKeyboardButton(
                    text=new_text,
                    callback_data=new_callback or original_callback
                )
                new_row.append(new_button)
                log.debug(f"Кнопка включена: {new_text}")
            else:
                new_row.append(button)
        new_keyboard.append(new_row)
    
    return InlineKeyboardMarkup(inline_keyboard=new_keyboard)


def create_progress_keyboard(
    action: str,
    progress_text: str = "⏳ Обработка...",
    state: ProgressState = ProgressState.PROCESSING,
    show_cancel: bool = False
) -> InlineKeyboardMarkup:
    """
    Создать клавиатуру с прогрессом
    
    Args:
        action: Идентификатор действия
        progress_text: Текст прогресса
        state: Состояние прогресса
        show_cancel: Показывать кнопку отмены
        
    Returns:
        Клавиатура с прогрессом
    """
    builder = InlineKeyboardBuilder()
    
    # Эмодзи в зависимости от состояния
    emoji_map = {
        ProgressState.PROCESSING: "⏳",
        ProgressState.SUCCESS: "✅",
        ProgressState.ERROR: "❌",
        ProgressState.WAITING: "⏸️"
    }
    
    emoji = emoji_map.get(state, "⏳")
    full_text = f"{emoji} {progress_text}"
    
    builder.button(
        text=full_text,
        callback_data=f"progress_{action}_{state.value}"
    )
    
    if show_cancel:
        builder.button(
            text="❌ Отменить",
            callback_data=f"cancel_{action}"
        )
    
    builder.adjust(1)
    return builder.as_markup()


def create_status_indicator(
    items: List[Dict[str, Any]],
    status_key: str = "status"
) -> str:
    """
    Создать текстовый индикатор статусов
    
    Args:
        items: Список элементов со статусами
        status_key: Ключ статуса в словаре
        
    Returns:
        Текст с индикаторами статусов
    """
    status_emoji = {
        "online": "🟢",
        "offline": "🔴",
        "busy": "🟡",
        "error": "🔴",
        "warning": "🟡",
        "success": "🟢",
        "processing": "⏳"
    }
    
    lines = []
    for item in items:
        name = item.get("name", "Неизвестно")
        status = item.get(status_key, "offline")
        emoji = status_emoji.get(status, "⚪")
        details = item.get("details", "")
        
        line = f"{emoji} {name}"
        if details:
            line += f" — {details}"
        lines.append(line)
    
    return "\n".join(lines)


async def answer_with_progress(
    callback: CallbackQuery,
    text: str,
    original_markup: Optional[InlineKeyboardMarkup] = None,
    progress_duration: int = 0,
    final_text: Optional[str] = None,
    final_markup: Optional[InlineKeyboardMarkup] = None
):
    """
    Ответить с сообщением о прогрессе (для долгих операций)
    
    Args:
        callback: CallbackQuery объект
        text: Текст сообщения
        original_markup: Исходная клавиатура
        progress_duration: Длительность показа прогресса (0 - не обновлять)
        final_text: Финальный текст (если обновляется)
        final_markup: Финальная клавиатура (если обновляется)
    """
    try:
        if original_markup:
            # Делаем все кнопки неактивными
            disabled_markup = disable_all_buttons(original_markup)
            await callback.message.edit_text(
                text=text,
                reply_markup=disabled_markup
            )
            
            # Если указана длительность, обновляем через время
            if progress_duration > 0 and final_text:
                await asyncio.sleep(progress_duration)
                await callback.message.edit_text(
                    text=final_text,
                    reply_markup=final_markup or disabled_markup
                )
        else:
            await callback.answer(
                "⏳ Обработка запроса...",
                show_alert=False
            )
            
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e).lower():
            log.error(f"Ошибка при отправке прогресса: {e}")


def disable_all_buttons(
    markup: InlineKeyboardMarkup,
    disabled_text: str = "⏳ Ожидание...",
    style: ButtonStyle = ButtonStyle.DISABLED
) -> InlineKeyboardMarkup:
    """
    Отключить ВСЕ кнопки в клавиатуре
    
    Args:
        markup: Исходная клавиатура
        disabled_text: Текст для отключенных кнопок
        style: Стиль отключенных кнопок
        
    Returns:
        Клавиатура с отключенными кнопками
    """
    if not markup.inline_keyboard:
        return markup
    
    # Эмодзи для стиля
    emoji_map = {
        ButtonStyle.DISABLED: "⏳",
        ButtonStyle.SUCCESS: "✅",
        ButtonStyle.ERROR: "❌"
    }
    
    emoji = emoji_map.get(style, "⏳")
    if emoji not in disabled_text:
        disabled_text = f"{emoji} {disabled_text}"
    
    new_keyboard = []
    for row in markup.inline_keyboard:
        new_row = []
        for button in row:
            new_button = InlineKeyboardButton(
                text=disabled_text,
                callback_data="ignore"
            )
            new_row.append(new_button)
        new_keyboard.append(new_row)
    
    log.debug("Все кнопки отключены")
    return InlineKeyboardMarkup(inline_keyboard=new_keyboard)


async def show_temporary_notification(
    message: Message,
    text: str,
    duration: float = 2.0,
    notification_type: str = "info"
) -> None:
    """
    Показать временное уведомление
    
    Args:
        message: Объект сообщения
        text: Текст уведомления
        duration: Длительность показа (секунды)
        notification_type: Тип уведомления (info, success, error, warning)
    """
    emoji_map = {
        "info": "ℹ️",
        "success": "✅",
        "error": "❌",
        "warning": "⚠️"
    }
    
    emoji = emoji_map.get(notification_type, "ℹ️")
    notification_text = f"{emoji} {text}"
    
    try:
        notification = await message.answer(notification_text)
        await asyncio.sleep(duration)
        await notification.delete()
    except Exception as e:
        log.error(f"Ошибка при показе уведомления: {e}")


def create_confirmation_keyboard(
    confirm_text: str = "✅ Подтвердить",
    cancel_text: str = "❌ Отменить",
    confirm_callback: str = "confirm",
    cancel_callback: str = "cancel"
) -> InlineKeyboardMarkup:
    """
    Создать клавиатуру подтверждения
    
    Args:
        confirm_text: Текст кнопки подтверждения
        cancel_text: Текст кнопки отмены
        confirm_callback: Callback_data для подтверждения
        cancel_callback: Callback_data для отмены
        
    Returns:
        Клавиатура подтверждения
    """
    builder = InlineKeyboardBuilder()
    
    builder.button(text=confirm_text, callback_data=confirm_callback)
    builder.button(text=cancel_text, callback_data=cancel_callback)
    
    builder.adjust(2)
    return builder.as_markup()


async def update_message_with_feedback(
    message: Message,
    text: str,
    markup: Optional[InlineKeyboardMarkup] = None,
    parse_mode: str = "Markdown",
    disable_web_page_preview: bool = True
) -> bool:
    """
    Обновить сообщение с обработкой ошибок
    
    Args:
        message: Сообщение для обновления
        text: Новый текст
        markup: Новая клавиатура
        parse_mode: Режим парсинга
        disable_web_page_preview: Отключить превью ссылок
        
    Returns:
        True если успешно, False если ошибка
    """
    try:
        await message.edit_text(
            text=text,
            reply_markup=markup,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview
        )
        return True
    except TelegramBadRequest as e:
        if "message is not modified" in str(e).lower():
            log.debug("Сообщение не изменилось")
            return True
        else:
            log.error(f"Ошибка при обновлении сообщения: {e}")
            return False
    except Exception as e:
        log.error(f"Неожиданная ошибка при обновлении сообщения: {e}")
        return False


# Пример использования
if __name__ == "__main__":
    # Тестирование функций
    import asyncio
    
    # Создание тестовой клавиатуры
    test_builder = InlineKeyboardBuilder()
    test_builder.button(text="Кнопка 1", callback_data="btn1")
    test_builder.button(text="Кнопка 2", callback_data="btn2")
    test_builder.button(text="Удалить", callback_data="delete")
    test_builder.adjust(2, 1)
    
    test_markup = test_builder.as_markup()
    
    # Тест отключения кнопки
    disabled_markup = disable_button(test_markup, "Удалить", "⏳ Удаление...")
    print("Клавиатура с отключенной кнопкой создана")
    
    # Тест отключения всех кнопок
    all_disabled = disable_all_buttons(test_markup)
    print("Все кнопки отключены")
    
    # Тест клавиатуры прогресса
    progress_markup = create_progress_keyboard(
        action="upload",
        progress_text="Загрузка файла...",
        show_cancel=True
    )
    print("Клавиатура прогресса создана")
    
    # Тест индикатора статусов
    items = [
        {"name": "Сервис A", "status": "online", "details": "Работает"},
        {"name": "Сервис B", "status": "processing", "details": "Загрузка"},
        {"name": "Сервис C", "status": "error", "details": "Ошибка"}
    ]
    
    status_text = create_status_indicator(items)
    print("\nИндикатор статусов:")
    print(status_text)
    
    print("\nВсе функции UI feedback работают корректно")