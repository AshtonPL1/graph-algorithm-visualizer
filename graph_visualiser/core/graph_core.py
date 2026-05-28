"""
Graph wrapper using networkx. Provides validation and helper properties.

Обёртка графа на основе networkx. Предоставляет валидацию и вспомогательные свойства.
"""

from typing import Any, Dict, Tuple

import networkx as nx


class GraphConfig:
    """
    Holds a networkx graph and metadata like presence of coordinates.

    Хранит граф networkx и метаданные, например, наличие координат.
    """
    def __init__(self, graph: nx.Graph, has_coordinates: bool = True):
        self.graph = graph
        self.has_coordinates = has_coordinates

    def get_pos(self) -> Dict[Any, Tuple[float, float]]:
        """
        Returns positions of all vertices as a dict {node: (x, y)}.

        Возвращает позиции всех вершин в виде словаря {вершина: (x, y)}.
        """
        if not self.has_coordinates:
            # Fallback layout (spring) for visualization
            # Запасная раскладка (spring) для визуализации
            return nx.spring_layout(self.graph, seed=42)
        return nx.get_node_attributes(self.graph, 'pos')

    def validate_vertices(self, start: str, end: str) -> None:
        """
        Raises ValueError if start or end vertex is missing in graph.

        Вызывает ValueError, если стартовая или конечная вершина отсутствует в графе.
        """
        if start not in self.graph:
            raise ValueError(f"Start vertex '{start}' not found in graph.")
        if end not in self.graph:
            raise ValueError(f"End vertex '{end}' not found in graph.")

    @property
    def nodes(self):
        return self.graph.nodes

    @property
    def edges(self):
        return self.graph.edges

    def __repr__(self):
        return (f"GraphConfig(nodes={len(self.graph.nodes)}, "
                f"edges={len(self.graph.edges)}, "
                f"coords={self.has_coordinates})")