"""
Tests for AlgorithmState dataclass.

Тесты для класса данных AlgorithmState.
"""

import unittest
from graph_visualiser.core.state import AlgorithmState


class TestAlgorithmState(unittest.TestCase):
    def test_default_creation(self):
        state = AlgorithmState()
        self.assertIsInstance(state.visited, set)
        self.assertEqual(len(state.visited), 0)
        self.assertIsNone(state.current_vertex)
        self.assertIsNone(state.final_path)
        self.assertFalse(state.done)
        self.assertFalse(state.improved)
        self.assertIsNone(state.improved_vertex)

    def test_custom_fields(self):
        state = AlgorithmState(
            visited={"A", "B"},
            dist={"A": 0.0, "B": 5.0},
            parent={"A": None, "B": "A"},
            current_vertex="B",
            relax_edge=("B", "C"),
            f_values={"A": 10.0, "B": 8.0},
            final_path=["A", "B"],
            done=True,
            improved=True,
            improved_vertex="C"
        )
        self.assertEqual(state.current_vertex, "B")
        self.assertTrue(state.done)
        self.assertEqual(state.improved_vertex, "C")
        self.assertTrue(state.improved)