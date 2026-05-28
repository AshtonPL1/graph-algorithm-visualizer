"""
Functions to export and import algorithm states to/from JSON files.

Функции для экспорта и импорта состояний алгоритма в/из JSON файлов.
"""

import json
from pathlib import Path
from typing import List

from ..core.state import AlgorithmState


def states_to_json(states: List[AlgorithmState], filepath: str) -> None:
    """
    Serialize a list of AlgorithmState objects to a JSON file.

    Сериализует список объектов AlgorithmState в файл JSON.

    Args:
        states: List of algorithm states to save.
        filepath: Output file path.
    """
    serializable = []
    for state in states:
        # Convert sets to lists for JSON; frozensets not directly serializable
        # Преобразуем множества в списки для JSON; frozenset не сериализуем напрямую
        serializable.append({
            "visited": list(state.visited),
            "dist": state.dist,
            "parent": {k: v for k, v in state.parent.items() if v is not None},  # omit None
            "current_vertex": state.current_vertex,
            "relax_edge": list(state.relax_edge) if state.relax_edge else None,
            "f_values": state.f_values,
            "final_path": state.final_path,
            "done": state.done,
            "improved": state.improved,
            "improved_vertex": state.improved_vertex,
        })
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False)


def json_to_states(filepath: str) -> List[AlgorithmState]:
    """
    Deserialize a JSON file back to a list of AlgorithmState objects.

    Десериализует JSON файл обратно в список объектов AlgorithmState.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    states = []
    for item in data:
        # Convert lists back to sets where needed
        # Преобразуем списки обратно в множества где необходимо
        states.append(AlgorithmState(
            visited=set(item["visited"]),
            dist=item["dist"],
            parent={k: v for k, v in item.get("parent", {}).items()},
            current_vertex=item["current_vertex"],
            relax_edge=tuple(item["relax_edge"]) if item["relax_edge"] else None,
            f_values=item.get("f_values"),
            final_path=item.get("final_path"),
            done=item["done"],
            improved=item.get("improved", False),
            improved_vertex=item.get("improved_vertex"),
        ))
    return states