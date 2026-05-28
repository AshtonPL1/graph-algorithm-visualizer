"""
Implementations of Dijkstra and A* algorithms as step-by-step generators.

Реализации алгоритмов Дейкстры и A* в виде пошаговых генераторов.
"""

import heapq
import math
from abc import ABC, abstractmethod
from typing import Generator, Dict, Optional, Set, Tuple

import networkx as nx

from .state import AlgorithmState


def reconstruct_path(parent: Dict[str, Optional[str]], start: str, target: str) -> Optional[list[str]]:
    """
    Reconstruct the path from start to target using the parent dictionary.
    Returns the list of vertices if a path exists, otherwise None.

    Восстанавливает путь от старта до цели с помощью словаря предшественников.
    Возвращает список вершин, если путь существует, иначе None.
    """
    if parent.get(target) is None and start != target:
        return None
    path = []
    curr = target
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()
    return path if path[0] == start else None


class ShortestPathAlgorithm(ABC):
    """
    Abstract base class for shortest path algorithms.

    Абстрактный базовый класс для алгоритмов поиска кратчайшего пути.
    """
    def __init__(self, G: nx.Graph):
        self.G = G

    @abstractmethod
    def run(self, start: str, target: str) -> Generator[AlgorithmState, None, None]:
        """
        Yields AlgorithmState objects representing each step of the algorithm.

        Возвращает генератор объектов AlgorithmState для каждого шага алгоритма.
        """
        ...


class DijkstraAlgorithm(ShortestPathAlgorithm):
    """
    Dijkstra's algorithm step-by-step generator.

    Пошаговый генератор алгоритма Дейкстры.
    """
    def run(self, start: str, target: str) -> Generator[AlgorithmState, None, None]:
        # Initialize distances and parents
        # Инициализация расстояний и предшественников
        dist: Dict[str, float] = {v: float('inf') for v in self.G.nodes}
        parent: Dict[str, Optional[str]] = {v: None for v in self.G.nodes}
        dist[start] = 0.0
        visited: Set[str] = set()
        pq: list[Tuple[float, str]] = [(0.0, start)]

        # Initial state (no current vertex)
        # Начальное состояние (нет текущей вершины)
        yield AlgorithmState(
            visited=set(),
            dist=dist.copy(),
            parent=parent.copy(),
            current_vertex=None,
            relax_edge=None,
            f_values=None,
            final_path=None,
            done=False,
            improved=False,
            improved_vertex=None
        )

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue  # outdated entry, skip without showing step
                # устаревшая запись, пропускаем без показа шага

            # Extraction step: mark u as visited and set as current
            # Шаг извлечения: помечаем u как посещённую и делаем текущей
            visited.add(u)
            yield AlgorithmState(
                visited=visited.copy(),
                dist=dist.copy(),
                parent=parent.copy(),
                current_vertex=u,
                relax_edge=None,
                f_values=None,
                final_path=None,
                done=False,
                improved=False,
                improved_vertex=None
            )

            if u == target:
                break  # target reached, will finalize after loop
                # цель достигнута, финализируем после цикла

            # Relaxation steps for each neighbor
            # Шаги релаксации для каждого соседа
            for v, edge_data in self.G[u].items():
                new_dist = dist[u] + edge_data['weight']
                improved = new_dist < dist[v]
                if improved:
                    dist[v] = new_dist
                    parent[v] = u
                    heapq.heappush(pq, (new_dist, v))
                # Yield relaxation step (whether improved or not)
                # Возвращаем шаг релаксации (независимо от улучшения)
                yield AlgorithmState(
                    visited=visited.copy(),
                    dist=dist.copy(),
                    parent=parent.copy(),
                    current_vertex=u,
                    relax_edge=(u, v),
                    f_values=None,
                    final_path=None,
                    done=False,
                    improved=improved,
                    improved_vertex=v if improved else None
                )

        # Final step: compute final path or mark as not found
        # Финальный шаг: вычисляем итоговый путь или помечаем как ненайденный
        final_path = reconstruct_path(parent, start, target)
        yield AlgorithmState(
            visited=visited,
            dist=dist,
            parent=parent,
            current_vertex=None,
            relax_edge=None,
            f_values=None,
            final_path=final_path if final_path else None,
            done=True,
            improved=False,
            improved_vertex=None
        )


class AStarAlgorithm(ShortestPathAlgorithm):
    """
    A* algorithm step-by-step generator.
    Requires vertex coordinates for heuristic calculation.

    Пошаговый генератор алгоритма A*.
    Требует координат вершин для вычисления эвристики.
    """
    def __init__(self, G: nx.Graph):
        super().__init__(G)
        # Ensure all nodes have 'pos' attribute
        # Убеждаемся, что все узлы имеют атрибут 'pos'
        for node in G.nodes:
            if 'pos' not in G.nodes[node]:
                raise ValueError(f"Node '{node}' missing 'pos' attribute, required for A*.")

    def _heuristic(self, u: str, target: str) -> float:
        """Euclidean distance heuristic. / Эвристика евклидова расстояния."""
        ux, uy = self.G.nodes[u]['pos']
        tx, ty = self.G.nodes[target]['pos']
        return math.sqrt((ux - tx) ** 2 + (uy - ty) ** 2)

    def run(self, start: str, target: str) -> Generator[AlgorithmState, None, None]:
        g_score: Dict[str, float] = {v: float('inf') for v in self.G.nodes}
        f_score: Dict[str, float] = {v: float('inf') for v in self.G.nodes}
        parent: Dict[str, Optional[str]] = {v: None for v in self.G.nodes}
        g_score[start] = 0.0
        f_score[start] = self._heuristic(start, target)
        visited: Set[str] = set()
        pq: list[Tuple[float, str]] = [(f_score[start], start)]

        # Initial state
        # Начальное состояние
        yield AlgorithmState(
            visited=set(),
            dist=g_score.copy(),  # dist field holds g values
            parent=parent.copy(),
            current_vertex=None,
            relax_edge=None,
            f_values=f_score.copy(),
            final_path=None,
            done=False,
            improved=False,
            improved_vertex=None
        )

        while pq:
            f_val, u = heapq.heappop(pq)
            if u in visited:
                continue

            # Extraction step
            # Шаг извлечения
            visited.add(u)
            yield AlgorithmState(
                visited=visited.copy(),
                dist=g_score.copy(),
                parent=parent.copy(),
                current_vertex=u,
                relax_edge=None,
                f_values=f_score.copy(),
                final_path=None,
                done=False,
                improved=False,
                improved_vertex=None
            )

            if u == target:
                break

            # Relaxation steps for neighbors
            # Шаги релаксации для соседей
            for v, edge_data in self.G[u].items():
                tentative_g = g_score[u] + edge_data['weight']
                improved = tentative_g < g_score[v]
                if improved:
                    g_score[v] = tentative_g
                    f_score[v] = tentative_g + self._heuristic(v, target)
                    parent[v] = u
                    heapq.heappush(pq, (f_score[v], v))
                yield AlgorithmState(
                    visited=visited.copy(),
                    dist=g_score.copy(),
                    parent=parent.copy(),
                    current_vertex=u,
                    relax_edge=(u, v),
                    f_values=f_score.copy(),
                    final_path=None,
                    done=False,
                    improved=improved,
                    improved_vertex=v if improved else None
                )

        final_path = reconstruct_path(parent, start, target)
        yield AlgorithmState(
            visited=visited,
            dist=g_score,
            parent=parent,
            current_vertex=None,
            relax_edge=None,
            f_values=f_score,
            final_path=final_path if final_path else None,
            done=True,
            improved=False,
            improved_vertex=None
        )