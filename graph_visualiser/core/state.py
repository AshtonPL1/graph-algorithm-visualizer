"""
Dataclass representing a single step of the shortest path algorithm.

Класс данных, представляющий один шаг алгоритма поиска кратчайшего пути.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, Set, Tuple, List


@dataclass
class AlgorithmState:
    """
    Immutable snapshot of algorithm structures at a given step.

    Неизменяемый снимок структур данных алгоритма на данном шаге.
    """
    visited: Set[str] = field(default_factory=set)
    # Set of vertices whose final distances are determined (extracted from queue).
    # Множество вершин с окончательными расстояниями (извлечённых из очереди).
    dist: Dict[str, float] = field(default_factory=dict)
    # Current known shortest distances from start (g for A*).
    # Текущие известные кратчайшие расстояния от старта (g для A*).
    parent: Dict[str, Optional[str]] = field(default_factory=dict)
    # Predecessor map for path reconstruction.
    # Карта предшественников для восстановления пути.
    current_vertex: Optional[str] = None
    # Vertex being processed (extracted from priority queue).
    # Вершина, обрабатываемая в данный момент (извлечённая из очереди с приоритетом).
    relax_edge: Optional[Tuple[str, str]] = None
    # Edge (u, v) currently undergoing relaxation, if any.
    # Ребро (u, v), в данный момент проходящее релаксацию, если есть.
    f_values: Optional[Dict[str, float]] = None
    # For A*: f(v) = g(v) + h(v) for all vertices.
    # Для A*: f(v) = g(v) + h(v) для всех вершин.
    final_path: Optional[List[str]] = None
    # The shortest path from start to target if found, else None.
    # Кратчайший путь от старта до цели, если найден, иначе None.
    done: bool = False
    # Flag indicating algorithm has completed.
    # Флаг, показывающий, что алгоритм завершён.
    improved: bool = False
    # Whether the last relaxation improved the distance.
    # Было ли улучшено расстояние на последней релаксации.
    improved_vertex: Optional[str] = None
    # The vertex whose distance was improved (if any).
    # Вершина, расстояние до которой улучшилось (если есть).