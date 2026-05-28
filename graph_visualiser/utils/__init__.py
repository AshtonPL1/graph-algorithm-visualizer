"""
Utility package: colors, settings, exceptions, helpers.

Вспомогательный пакет: цвета, настройки, исключения, помощники.
"""

from .colors import *
from .settings import *
from .exceptions import *

__all__ = [
    # from colors
    "VERTEX_DEFAULT", "VERTEX_VISITED", "VERTEX_CURRENT", "VERTEX_PATH",
    "EDGE_DEFAULT", "EDGE_RELAX", "EDGE_PATH",
    "TEXT_DARK", "TEXT_LIGHT", "PATH_MISSING_COLOR",
    "EDGE_DEFAULT_WIDTH", "EDGE_RELAX_WIDTH", "EDGE_PATH_WIDTH",
    "VERTEX_MARKER_SIZE", "FONT_SIZE_ID", "FONT_SIZE_DIST", "LABEL_OFFSET",
    # from settings
    "DEFAULT_SPEED_MS", "WINDOW_WIDTH", "WINDOW_HEIGHT", "WINDOW_DPI",
    "FALLBACK_LAYOUT", "MAX_VERTICES_PERFORMANCE", "MAX_EDGES_PERFORMANCE",
    "ENABLE_INTERACTIVE",
    # from exceptions
    "GraphError", "FileFormatError", "FileNotFoundErrorGraph",
    "MissingCoordinatesError", "VertexNotFoundError",
]