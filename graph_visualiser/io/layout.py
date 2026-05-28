"""
Functions to compute vertex positions when coordinates are missing.

Функции для вычисления позиций вершин, когда координаты отсутствуют.
"""

import networkx as nx


def compute_layout(G: nx.Graph, layout_name: str = "spring", seed: int = 42):
    """
    Computes node positions using a networkx layout algorithm.

    Вычисляет позиции узлов с помощью алгоритма раскладки networkx.

    Args:
        G: The graph.
        layout_name: One of 'spring', 'circular', 'kamada_kawai', etc.
        seed: Random seed for reproducible layouts.

    Returns:
        dict: {node: (x, y)} positions.
    """
    layout_func = getattr(nx, f"{layout_name}_layout", None)
    if layout_func is None:
        raise ValueError(f"Unknown layout: {layout_name}")
    return layout_func(G, seed=seed)