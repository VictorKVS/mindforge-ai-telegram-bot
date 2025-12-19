# AGENT PROFILE SPECIFICATION (APS) - INTERNAL VERSION

Этот документ описывает структуру профиля агента (profile.json) и правила отображения данных в зависимости от уровня доступа (0–6+).

## Основные файлы:
- profile.json — данные агента
- access_manager.py — механика уровней доступа
- profile_loader.py — загрузка и выдача профиля
- __init__.py — модуль профиля

## Структура profile.json
- agent_id
- agent_type
- display_name
- role
- current_level
- access[0..6]
- services
- skills
- inventory
- schedule

## Правила уровней
- Level 0 — скрыто
- Level 1 — минимальная информация
- Level 2 — базовый клиент
- Level 3 — рабочий доступ
- Level 4 — бригадир
- Level 5 — прораб
- Level 6 — директор / premium

## Использование
Профиль загружается через:
