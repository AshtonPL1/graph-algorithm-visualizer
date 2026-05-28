"""
Color constants for graph visualization.

Цветовые константы для визуализации графа.
"""

# Vertex colors (fill / edge)
# Цвета вершин (заливка / граница)
VERTEX_DEFAULT = "#D3D3D3"      # lightgrey — не посещена
VERTEX_VISITED = "#17BECF"      # teal — посещена
VERTEX_CURRENT = "#FFD700"      # gold — текущая обрабатываемая
VERTEX_PATH = "#FF7F0E"         # orange — в финальном пути

# Edge colors
# Цвета рёбер
EDGE_DEFAULT = "#888888"        # grey — обычное ребро
EDGE_RELAX = "#1F77B4"          # blue — релаксация на текущем шаге
EDGE_PATH = "#2CA02C"           # green — итоговый путь

# Text and annotation colors
# Цвета текста и подписей
TEXT_DARK = "#333333"
TEXT_LIGHT = "#FFFFFF"
PATH_MISSING_COLOR = "red"

# Additional style parameters
# Дополнительные параметры стиля
EDGE_DEFAULT_WIDTH = 1.5
EDGE_RELAX_WIDTH = 3.0
EDGE_PATH_WIDTH = 4.0
VERTEX_MARKER_SIZE = 600
FONT_SIZE_ID = 10
FONT_SIZE_DIST = 8
LABEL_OFFSET = 15

EDGE_RELAX_IMPROVED = "#FF4500"      # OrangeRed для улучшающего ребра
EDGE_RELAX_IMPROVED_WIDTH = 4.0
DIST_IMPROVED = "#2ca02c"            # зелёный для улучшенной метки расстояния