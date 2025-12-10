import json
import os

from src.bot.ai.llm_router import route
from src.bot.uag.rozetka_service import RozetkaService


TASK_DB_PATH = "tasks.json"

# ---------------------------------------------------------
# БАЗОВЫЕ ФУНКЦИИ ХРАНЕНИЯ ЗАДАЧ
# ---------------------------------------------------------

def load_tasks():
    if not os.path.exists(TASK_DB_PATH):
        return []
    try:
        with open(TASK_DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_tasks(tasks):
    with open(TASK_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def get_next_id(tasks):
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


# ---------------------------------------------------------
# БАЗОВЫЙ КЛАСС АГЕНТА
# ---------------------------------------------------------

class BaseAgent:
    category = None

    async def run(self, task):
        raise NotImplementedError


# ---------------------------------------------------------
# ОСНОВНЫЕ АГЕНТЫ
# ---------------------------------------------------------

class OSINTAgent(BaseAgent):
    category = "osint"

    async def run(self, task):
        q = task["task"]
        return await route(f"Проведи OSINT анализ задачи '{q}' в структурированном виде.")


class AnalysisAgent(BaseAgent):
    category = "analysis"

    async def run(self, task):
        q = task["task"]
        return await route(f"Проанализируй задачу '{q}' и дай конспектированный вывод.")


class LLMReasoningAgent(Base(BaseAgent)):
    category = "llm"

    async def run(self, task):
        q = task["task"]
        return await route(f"Реши задачу рассуждением: '{q}'. Дай CoT.")


class WorkflowAgent(BaseAgent):
    category = "workflow"

    async def run(self, task):
        q = task["task"]
        return await route(f"Разбей задачу '{q}' на шаги и предложи план выполнения.")


class InterviewAgent(BaseAgent):
    category = "interview"

    async def run(self, task):
        q = task["task"]
        return await route(f"Проанализируй навыки по теме '{q}', предложи обучение.")


# ---------------------------------------------------------
# ПОЛНОЦЕННЫЙ FOUNDATION AGENT — ЛЕНТОЧНЫЙ ФУНДАМЕНТ
# ---------------------------------------------------------

class FoundationAgent(BaseAgent):
    category = "build"

    async def run(self, task):
        """
        Ленточный фундамент 6×6 м
        Ширина ленты: 0.4 м
        Глубина: 1.5 м
        Высота: 1.0 м
        """

        length = 6.0
        width = 0.4
        height = 1.0
        depth = 1.5
        perimeter = 6 * 4  # 24 м

        # 1. Объём траншеи
        ditch_volume = perimeter * width * depth  # м3

        # 2. Надземная часть
        wall_volume = perimeter * width * height

        # 3. Бетон всего
        concrete_volume = ditch_volume + wall_volume

        # 4. Арматура
        rebar12_m = perimeter * 4

        hoop_count = int(perimeter / 0.4)
        hoop_perimeter = 2 * (1.0 + 0.4)
        rebar8_m = hoop_count * hoop_perimeter

        wire_kg = round(hoop_count * 0.03, 2)

        boards_per_side = height / 0.15
        boards_total = int((boards_per_side * perimeter) / 6)

        cement_bags = int(concrete_volume * 14)

        materials = [
            {"name": "арматура 12 мм", "amount": f"{rebar12_m:.1f} м"},
            {"name": "арматура 8 мм", "amount": f"{rebar8_m:.1f} м"},
            {"name": "вязальная проволока", "amount": f"{wire_kg} кг"},
            {"name": "доска 40×150", "amount": f"{boards_total} шт"},
            {"name": "цемент м500", "amount": f"{cement_bags} мешков"},
            {"name": "пескобетон м300", "amount": "по необходимости"},
            {"name": "гидроизоляция", "amount": f"{perimeter * 2} м"},
            {"name": "мастика", "amount": "1 ведро"}
        ]

        result_json = {
            "status": "ok",
            "task": task["task"],
            "foundation_type": "ленточный фундамент",
            "dimensions": {
                "length": length,
                "width": width,
                "height": height,
                "depth": depth
            },
            "volumes": {
                "ditch_m3": round(ditch_volume, 2),
                "wall_m3": round(wall_volume, 2),
                "concrete_m3": round(concrete_volume, 2)
            },
            "materials": materials
        }

        return json.dumps(result_json, ensure_ascii=False, indent=2)


# ---------------------------------------------------------
# МАРКЕТИНГОВЫЙ АГЕНТ — ПОДБОР ЦЕН ПО РОЗЕТКЕ
# ---------------------------------------------------------

class MarketPriceAgent(BaseAgent):
    category = "market"
    service = RozetkaService()

    async def run(self, task):
        """
        Получает список материалов (JSON),
        ищет цены по трём магазинам,
        возвращает дашборд.
        """

        try:
            data = json.loads(task["result"])
        except:
            return "Ошибка: агент получил некорректный JSON."

        items = data.get("materials", [])
        if not items:
            return "Материалы не найдены."

        response_lines = ["📊 <b>Сравнение цен по материалам:</b>\n"]

        for item in items:
            name = item["name"].lower()
            amount = item["amount"]

            stores = await self.service.query(name)

            if not stores:
                response_lines.append(f"❌ {name} — нет в наличии.\n")
                continue

            response_lines.append(f"🔹 <b>{name}</b> (нужно: {amount}):")

            for store in stores:
                response_lines.append(
                    f"   {store['store_name']}: {store['price']} ₽ "
                    f"(доставка {store['delivery_days']} д.)"
                )

            best = min(stores, key=lambda x: x["price"])
            response_lines.append(
                f"   👉 Лучшее предложение: <b>{best['store_name']}</b> — {best['price']} ₽\n"
            )

        return "\n".join(response_lines)


# ---------------------------------------------------------
# РЕЕСТР АГЕНТОВ
# ---------------------------------------------------------

AGENTS = {
    "osint": OSINTAgent(),
    "analysis": AnalysisAgent(),
    "llm": LLMReasoningAgent(),
    "workflow": WorkflowAgent(),
    "interview": InterviewAgent(),
    "build": FoundationAgent(),
    "market": MarketPriceAgent()
}


# ---------------------------------------------------------
# ВЫПОЛНЕНИЕ ЗАДАЧИ
# ---------------------------------------------------------

async def run_task(task_id: int):
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)

    if not task:
        return None, "Задача не найдена."

    agent = AGENTS.get(task["category"])
    if not agent:
        return None, f"Агент для категории '{task['category']}' не найден."

    task["status"] = "assigned"
    save_tasks(tasks)

    result = await agent.run(task)

    task["status"] = "completed"
    task["result"] = result
    save_tasks(tasks)

    return result, None
