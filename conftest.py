import sys
from pathlib import Path

# Путь к корню проекта
ROOT = Path(__file__).resolve().parent

# Путь к src/
SRC = ROOT / "src"

# Добавляем src в sys.path если его нет
if SRC.exists() and str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
