"""
Entry point: parses CLI arguments, loads graph, runs algorithm, starts visualization.

Точка входа: разбирает аргументы командной строки, загружает граф, запускает алгоритм, начинает визуализацию.
"""

import sys
import argparse
from typing import List

from .core.algorithms import DijkstraAlgorithm, AStarAlgorithm
from .core.state import AlgorithmState
from .io.graph_reader import load_graph_from_file, input_graph_manually
from .io.state_exporter import states_to_json, json_to_states
from .utils.exceptions import (
    GraphError,
    FileNotFoundErrorGraph,
    FileFormatError,
    MissingCoordinatesError,
    VertexNotFoundError,
)
from .utils.settings import DEFAULT_SPEED_MS
from .viz.animator import GraphAnimator


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Разбирает аргументы командной строки.
    """
    parser = argparse.ArgumentParser(
        description="Graph Algorithm Visualizer (Dijkstra, A*) with step-by-step animation"
    )
    parser.add_argument("--start", type=str, help="Start vertex ID")
    parser.add_argument("--end", type=str, help="Target vertex ID")
    parser.add_argument("--file", type=str, help="Path to graph file")
    parser.add_argument(
        "--algo", choices=["dijkstra", "astar"], default="dijkstra",
        help="Algorithm to use (default: dijkstra)"
    )
    parser.add_argument(
        "--speed", type=int, default=DEFAULT_SPEED_MS,
        help=f"Animation delay between frames in milliseconds (default: {DEFAULT_SPEED_MS})"
    )
    # Export / save / load states (mutually exclusive)
    export_group = parser.add_mutually_exclusive_group()
    export_group.add_argument("--export", type=str, default=None,
                              help="Export animation to file (.gif or .mp4) instead of interactive window.")
    export_group.add_argument("--save-states", type=str, default=None,
                              help="Save algorithm states to a JSON file and exit.")
    export_group.add_argument("--load-states", type=str, default=None,
                              help="Load algorithm states from a JSON file (requires --file and --algo).")

    return parser.parse_args()


def main() -> None:
    """
    Main function: orchestrates the workflow.

    Основная функция: управляет рабочим процессом.
    """
    args = parse_args()

    # ------------------------------------------------------------
    # Load or generate algorithm states
    # Загрузка или генерация состояний алгоритма
    # ------------------------------------------------------------
    if args.load_states:
        # Load states from JSON; graph file and algo must still be provided
        if not args.file:
            print("Error: --file is required when loading states to provide graph structure.", file=sys.stderr)
            sys.exit(1)
        graph_config = load_graph_from_file(args.file)
        states = json_to_states(args.load_states)
        algo_name = "Dijkstra" if args.algo == "dijkstra" else "A*"
    else:
        # Normal flow: load graph and run algorithm
        if not args.start or not args.end:
            print("Error: --start and --end are required when running an algorithm.", file=sys.stderr)
            sys.exit(1)

        # Load graph from file or manual input
        try:
            if args.file:
                graph_config = load_graph_from_file(args.file)
            else:
                graph_config = input_graph_manually()
        except FileNotFoundErrorGraph as e:
            print(f"Error: {e.message}", file=sys.stderr)
            sys.exit(e.exit_code)
        except FileFormatError as e:
            print(f"Error: {e.message}", file=sys.stderr)
            sys.exit(e.exit_code)
        except KeyboardInterrupt:
            print("\nInput interrupted. Exiting.")
            sys.exit(0)
        except Exception as e:
            print(f"Unexpected error during graph loading: {e}", file=sys.stderr)
            sys.exit(1)

        G = graph_config.graph
        has_coords = graph_config.has_coordinates

        # Validate start/end vertices exist
        try:
            graph_config.validate_vertices(args.start, args.end)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(6)

        # Choose algorithm
        if args.algo == "astar":
            if not has_coords:
                print("Error: Algorithm A* requires vertex coordinates.", file=sys.stderr)
                sys.exit(5)
            algo = AStarAlgorithm(G)
        else:
            algo = DijkstraAlgorithm(G)

        # Generate states
        try:
            states: List[AlgorithmState] = list(algo.run(args.start, args.end))
        except Exception as e:
            print(f"Error during algorithm execution: {e}", file=sys.stderr)
            sys.exit(1)

        algo_name = "Dijkstra" if args.algo == "dijkstra" else "A*"

        # If --save-states, save JSON and exit
        if args.save_states:
            try:
                states_to_json(states, args.save_states)
                print(f"Algorithm states saved to {args.save_states}")
                sys.exit(0)
            except Exception as e:
                print(f"Error saving states: {e}", file=sys.stderr)
                sys.exit(1)

    # ------------------------------------------------------------
    # Visualization or export
    # Визуализация или экспорт
    # ------------------------------------------------------------
    G = graph_config.graph
    has_coords = graph_config.has_coordinates

    try:
        animator = GraphAnimator(
            G=G,
            states=states,
            speed_ms=args.speed,
            algo_name=algo_name,
            has_coordinates=has_coords,
        )
        if args.export:
            animator.save_animation(args.export)
        else:
            animator.animate()
    except KeyboardInterrupt:
        print("\nAnimation interrupted. Exiting.")
        sys.exit(0)
    except Exception as e:
        print(f"Error during visualization: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()