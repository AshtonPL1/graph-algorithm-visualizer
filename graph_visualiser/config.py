"""
Global project configuration constants.

Глобальные константы конфигурации проекта.
"""

from pathlib import Path

# Project root directory (where config.py resides)
# Корневая директория проекта (где находится config.py)
ROOT_DIR = Path(__file__).parent

# Default data directory for sample graphs
# Директория по умолчанию для графов-образцов
DATA_DIR = ROOT_DIR / "data"

# Default output directory for exports (if needed)
# Директория по умолчанию для экспорта (если потребуется)
OUTPUT_DIR = ROOT_DIR / "output"

# Ensure directories exist (optional, can be created lazily)
# Гарантировать существование директорий (опционально, можно создавать лениво)
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Supported algorithms
# Поддерживаемые алгоритмы
SUPPORTED_ALGORITHMS = ("dijkstra", "astar")