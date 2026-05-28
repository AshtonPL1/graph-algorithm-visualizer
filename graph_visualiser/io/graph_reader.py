"""
Functions to load a graph from a text file or manual console input.

Функции для загрузки графа из текстового файла или ручного консольного ввода.
"""

import sys
from typing import Dict, List, Tuple, TextIO

import networkx as nx

from ..core.graph_core import GraphConfig
from ..utils.exceptions import (
    FileFormatError,
    FileNotFoundErrorGraph,
    VertexNotFoundError,
)


def load_graph_from_file(filepath: str) -> GraphConfig:
    """
    Reads, parses, and validates a graph file. Returns a GraphConfig instance.

    Читает, разбирает и проверяет файл графа. Возвращает экземпляр GraphConfig.

    Supports two vertex formats:
        - With coordinates:   <ID> <X> <Y>   (all vertices must have coords)
        - Without coordinates: <ID>           (only IDs, coords computed later)

    A* requires coordinates; Dijkstra works with both.

    Поддерживает два формата вершин:
        - С координатами:   <ID> <X> <Y>   (все вершины должны иметь координаты)
        - Без координат:    <ID>           (только ID, координаты вычисляются позже)

    A* требует координаты; Дейкстра работает с обоими.

    Raises:
        FileNotFoundErrorGraph: if the file does not exist.
        FileFormatError: if the file content violates the required format.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise FileNotFoundErrorGraph(filepath)

    # Remove comment lines (starting with #) and empty lines, keeping track of original line numbers
    # Удаляем строки-комментарии (начинающиеся с #) и пустые строки, отслеживая исходные номера строк
    cleaned_lines = []
    line_numbers = []  # original line numbers for error reporting
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped and not stripped.startswith('#'):
            cleaned_lines.append(stripped)
            line_numbers.append(i)

    # Find section headers
    # Находим заголовки секций
    try:
        vertices_idx = cleaned_lines.index("VERTICES")
        edges_idx = cleaned_lines.index("EDGES")
    except ValueError as e:
        missing_section = str(e).split()[-1]  # 'VERTICES' or 'EDGES'
        raise FileFormatError(f"Missing section header: {missing_section}")

    if vertices_idx > edges_idx:
        raise FileFormatError("VERTICES section must precede EDGES section.")

    # Parse vertices, detect if coordinates are present
    # Разбираем вершины, определяем наличие координат
    vertices: Dict[str, Tuple[float, float] | None] = {}  # id -> (x,y) or None
    has_coords = None  # will be set based on first vertex format
    vertex_lines = cleaned_lines[vertices_idx + 1:edges_idx]
    for j, line in enumerate(vertex_lines):
        orig_line_no = line_numbers[vertices_idx + 1 + j]
        parts = line.split()
        if len(parts) == 1:
            # Format: only ID, no coordinates
            # Формат: только ID, без координат
            if has_coords is True:
                raise FileFormatError(
                    f"Inconsistent vertex format: expected coordinates for vertex '{parts[0]}'.",
                    line_number=orig_line_no
                )
            has_coords = False
            v_id = parts[0]
            if v_id in vertices:
                raise FileFormatError(
                    f"Duplicate vertex ID '{v_id}'.",
                    line_number=orig_line_no
                )
            vertices[v_id] = None  # no position
        elif len(parts) == 3:
            # Format: ID X Y
            # Формат: ID X Y
            if has_coords is False:
                raise FileFormatError(
                    f"Inconsistent vertex format: vertex '{parts[0]}' has coordinates, but previous vertices did not.",
                    line_number=orig_line_no
                )
            has_coords = True
            v_id, x_str, y_str = parts
            if v_id in vertices:
                raise FileFormatError(
                    f"Duplicate vertex ID '{v_id}'.",
                    line_number=orig_line_no
                )
            try:
                x = float(x_str)
                y = float(y_str)
            except ValueError:
                raise FileFormatError(
                    f"Invalid coordinates for vertex '{v_id}': ({x_str}, {y_str})",
                    line_number=orig_line_no
                )
            vertices[v_id] = (x, y)
        else:
            raise FileFormatError(
                f"Invalid vertex format. Expected '<ID>' or '<ID> <X> <Y>', got '{line}'",
                line_number=orig_line_no
            )

    # Parse edges (unchanged logic, but allow edges between vertices without coords)
    # Разбираем рёбра (логика без изменений, разрешены рёбра между вершинами без координат)
    edge_set = set()
    edges = []
    edge_lines = cleaned_lines[edges_idx + 1:]
    for j, line in enumerate(edge_lines):
        orig_line_no = line_numbers[edges_idx + 1 + j]
        parts = line.split()
        if len(parts) != 3:
            raise FileFormatError(
                f"Invalid edge format. Expected '<u> <v> <weight>', got '{line}'",
                line_number=orig_line_no
            )
        u, v, w_str = parts
        if u not in vertices:
            raise FileFormatError(
                f"Edge refers to non-existent vertex '{u}'.",
                line_number=orig_line_no
            )
        if v not in vertices:
            raise FileFormatError(
                f"Edge refers to non-existent vertex '{v}'.",
                line_number=orig_line_no
            )
        if u == v:
            raise FileFormatError(
                f"Loops are not allowed: '{u}' -> '{v}'.",
                line_number=orig_line_no
            )
        try:
            weight = float(w_str)
        except ValueError:
            raise FileFormatError(
                f"Invalid weight '{w_str}'.",
                line_number=orig_line_no
            )
        if weight <= 0:
            raise FileFormatError(
                f"Weight must be positive, got {weight}.",
                line_number=orig_line_no
            )
        pair = frozenset((u, v))
        if pair in edge_set:
            raise FileFormatError(
                f"Duplicate edge between '{u}' and '{v}'.",
                line_number=orig_line_no
            )
        edge_set.add(pair)
        edges.append((u, v, weight))

    # Build networkx Graph
    # Строим граф networkx
    G = nx.Graph()
    for v_id, pos in vertices.items():
        if pos is not None:
            G.add_node(v_id, pos=pos)
        else:
            G.add_node(v_id)  # no pos attribute; layout will be computed later
    G.add_weighted_edges_from(edges, weight='weight')

    return GraphConfig(G, has_coordinates=has_coords if has_coords is not None else False)


def input_graph_manually() -> GraphConfig:
    """
    Interactively reads graph data from the console.
    Always asks for coordinates, so has_coordinates = True.

    Интерактивно считывает данные графа из консоли.
    Всегда запрашивает координаты, поэтому has_coordinates = True.
    """
    print("Manual graph input mode.\n")

    while True:
        try:
            n = int(input("Enter number of vertices (positive integer): "))
            if n <= 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter a positive integer.")

    vertices = {}
    for i in range(1, n + 1):
        while True:
            v_id = input(f"Vertex {i} ID (no spaces): ").strip()
            if ' ' in v_id or not v_id:
                print("ID must be non-empty and contain no spaces.")
                continue
            if v_id in vertices:
                print(f"ID '{v_id}' already used. Choose another.")
                continue
            break
        while True:
            try:
                x = float(input(f"  X coordinate for {v_id}: "))
                y = float(input(f"  Y coordinate for {v_id}: "))
                break
            except ValueError:
                print("Coordinates must be real numbers.")
        vertices[v_id] = (x, y)

    while True:
        try:
            m = int(input("\nEnter number of edges (non-negative integer): "))
            if m < 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid input. Please enter a non-negative integer.")

    edges = []
    edge_set = set()
    for j in range(1, m + 1):
        while True:
            u = input(f"Edge {j} - first vertex ID: ").strip()
            if u not in vertices:
                print(f"Vertex '{u}' does not exist. Try again.")
                continue
            v = input(f"Edge {j} - second vertex ID: ").strip()
            if v not in vertices:
                print(f"Vertex '{v}' does not exist. Try again.")
                continue
            if u == v:
                print("Loops are not allowed. Enter distinct vertices.")
                continue
            pair = frozenset((u, v))
            if pair in edge_set:
                print("This edge already exists. Duplicate edges are not allowed.")
                continue
            while True:
                try:
                    w = float(input(f"  Weight for edge ({u}-{v}): "))
                    if w <= 0:
                        raise ValueError
                    break
                except ValueError:
                    print("Weight must be a positive number.")
            edge_set.add(pair)
            edges.append((u, v, w))
            break

    G = nx.Graph()
    for v_id, (x, y) in vertices.items():
        G.add_node(v_id, pos=(x, y))
    G.add_weighted_edges_from(edges, weight='weight')

    return GraphConfig(G, has_coordinates=True)