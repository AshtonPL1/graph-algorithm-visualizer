"""
Core package: graph representation, algorithm state, and algorithms.

Основной пакет: представление графа, состояние алгоритма и алгоритмы.
"""

from .state import AlgorithmState
from .graph_core import GraphConfig
from .algorithms import DijkstraAlgorithm, AStarAlgorithm

__all__ = [
    "AlgorithmState",
    "GraphConfig",
    "DijkstraAlgorithm",
    "AStarAlgorithm",
]