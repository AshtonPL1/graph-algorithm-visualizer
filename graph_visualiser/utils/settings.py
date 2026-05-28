"""
Default settings and tunable parameters for the application.

Настройки по умолчанию и изменяемые параметры приложения.
"""

# Animation defaults
# Параметры анимации по умолчанию
DEFAULT_SPEED_MS = 500          # интервал между кадрами в миллисекундах
WINDOW_WIDTH = 10               # дюймы
WINDOW_HEIGHT = 8               # дюймы
WINDOW_DPI = 100                # разрешение экрана по умолчанию

# Layout fallback (when no coordinates provided, for Dijkstra only)
# Запасная раскладка (если координаты не заданы, только для Дейкстры)
FALLBACK_LAYOUT = "spring"      # networkx layout function name

# Maximum vertices/edges for performance guarantees
# Максимальное число вершин/рёбер для гарантий производительности
MAX_VERTICES_PERFORMANCE = 500
MAX_EDGES_PERFORMANCE = 2000

# Interactive mode (to be used later with matplotlib buttons)
# Интерактивный режим (будет использоваться позже с кнопками matplotlib)
ENABLE_INTERACTIVE = False

# Animation export settings
# Настройки экспорта анимации
EXPORT_DPI = 100            # разрешение для сохраняемой анимации
EXPORT_FPS = 1000 / DEFAULT_SPEED_MS if DEFAULT_SPEED_MS > 0 else 2  # кадров в секунду на основе скорости