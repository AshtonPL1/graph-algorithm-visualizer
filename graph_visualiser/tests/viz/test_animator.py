"""
Tests for GraphAnimator drawing logic (headless).

Тесты для логики отрисовки GraphAnimator (без GUI).
"""

import unittest
import matplotlib
matplotlib.use('Agg')  # headless backend, must be before importing pyplot
import matplotlib.pyplot as plt
import networkx as nx

from graph_visualiser.core.state import AlgorithmState
from graph_visualiser.viz.animator import GraphAnimator


class TestGraphAnimator(unittest.TestCase):
    def setUp(self):
        # Create a simple graph with coordinates
        self.G = nx.Graph()
        self.G.add_node("A", pos=(0, 0))
        self.G.add_node("B", pos=(10, 0))
        self.G.add_node("C", pos=(5, 5))
        self.G.add_edge("A", "B", weight=5.0)
        self.G.add_edge("B", "C", weight=5.0)
        self.G.add_edge("C", "A", weight=7.0)

        # Build some algorithm states covering different phases
        self.states = [
            AlgorithmState(visited=set(), dist={"A": 0.0, "B": float('inf'), "C": float('inf')},
                           parent={"A": None, "B": None, "C": None},
                           current_vertex=None, done=False),
            AlgorithmState(visited={"A"}, dist={"A": 0.0, "B": 5.0, "C": float('inf')},
                           parent={"A": None, "B": "A", "C": None},
                           current_vertex="A", relax_edge=("A", "B"),
                           improved=True, improved_vertex="B", done=False),
            AlgorithmState(visited={"A", "B"}, dist={"A": 0.0, "B": 5.0, "C": 10.0},
                           parent={"A": None, "B": "A", "C": "B"},
                           current_vertex="B", relax_edge=("B", "C"),
                           improved=True, improved_vertex="C", done=False),
            AlgorithmState(visited={"A", "B", "C"}, dist={"A": 0.0, "B": 5.0, "C": 10.0},
                           parent={"A": None, "B": "A", "C": "B"},
                           final_path=["A", "B", "C"], done=True),
        ]
        self.animator = GraphAnimator(
            G=self.G,
            states=self.states,
            speed_ms=500,
            algo_name="Dijkstra",
            has_coordinates=True,
        )

    def tearDown(self):
        plt.close('all')

    def test_initialization(self):
        self.assertIsNotNone(self.animator.fig)
        self.assertIsNotNone(self.animator.ax)
        self.assertEqual(self.animator.marker_size, 600)  # n=3 -> small graph defaults
        self.assertTrue(self.animator.paused)

    def test_draw_first_frame(self):
        # просто проверим, что отрисовка не вызывает исключений
        try:
            self.animator._draw_frame(self.states[0], 0)
        except Exception as e:
            self.fail(f"_draw_frame raised exception: {e}")

    def test_draw_relax_frame(self):
        try:
            self.animator._draw_frame(self.states[1], 1)
        except Exception as e:
            self.fail(f"_draw_frame raised exception on relax frame: {e}")

    def test_draw_final_path(self):
        try:
            self.animator._draw_frame(self.states[3], 3)
        except Exception as e:
            self.fail(f"_draw_frame raised exception on final frame: {e}")

    def test_adaptive_scaling_large_graph(self):
        # Create a large graph to trigger scaling
        G_large = nx.Graph()
        for i in range(50):
            G_large.add_node(str(i), pos=(i, i))
        anim_large = GraphAnimator(G_large, self.states[:1], 500, "Dijkstra", has_coordinates=True)
        self.assertLess(anim_large.marker_size, 600)   # должно уменьшиться
        self.assertLess(anim_large.font_id, 10)
        plt.close('all')