import json
import os
from src.bot.ai.llm_router import route

TASK_DB = "data/tasks.json"


# ---------------------------
# загрузка / сохранение
# ---------------------------
def load_tasks():
    if not os.path.exists(TASK_DB):
        return []
    with open(TASK_DB, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []


def save_tasks(tasks):
    with open(TASK_DB, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def get_next_id(tasks):
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


# ---------------------------
# авто-категоризация (через LLM)
# ---------------------------
async def auto_categorize(text: str) -> str:
    prompt = (
        "Определи категорию задачи одного слова из списка: "
        "market, osint, analysis, llm, workflow, build.\n"
        f"Задача: {text}\nТолько одно слово:"
    )

    answer = await route(prompt)
    answer = answer.lower()

    for c in ["market", "osint", "analysis", "llm", "workflow", "build"]:
        if c in answer:
            return c

    return "llm"   # fallback


# ---------------------------
# выполнение задачи
# ---------------------------
async def run_task(task_id: int):
    tasks = load_tasks()
    task = next((t for t in tasks if t["id"] == task_id), None)

    if not task:
        return None, "Задача не найдена"

    task["status"] = "running"
    save_tasks(tasks)

    try:
        # основной вызов LLM
        prompt = f"Выполни задачу: {task['task']}"
        result = await route(prompt)

        task["status"] = "done"
        task["result"] = result
        save_tasks(tasks)

        return result, None

    except Exception as e:
        task["status"] = "error"
        task["result"] = str(e)
        save_tasks(tasks)
        return None, str(e)
