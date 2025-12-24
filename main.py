import sys
import os

# Добавляем src в PYTHONPATH
src_path = os.path.join(os.path.dirname(__file__), 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from agent.entrypoint import run_agent

if __name__ == "__main__":
    print("🚀 Запуск MindForge AI Telegram Agent...")
    result = run_agent("Сколько стоит цемент М500?")
    print(result)