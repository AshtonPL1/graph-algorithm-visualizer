"""
Tests for state JSON export/import.

Тесты для экспорта/импорта состояний в JSON.
"""

import unittest
import tempfile
import os
from graph_visualiser.core.state import AlgorithmState
from graph_visualiser.io.state_exporter import states_to_json, json_to_states


class TestStateExporter(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_roundtrip(self):
        states = [
            AlgorithmState(visited={"A"}, dist={"A": 0.0}, parent={"A": None}, done=False),
            AlgorithmState(visited={"A", "B"}, dist={"A": 0.0, "B": 5.0}, parent={"A": None, "B": "A"},
                           current_vertex="B", improved=True, improved_vertex="B", done=False),
            AlgorithmState(visited={"A", "B", "C"}, dist={"A": 0.0, "B": 5.0, "C": 8.0},
                           final_path=["A", "B", "C"], done=True)
        ]
        path = os.path.join(self.tmpdir.name, "states.json")
        states_to_json(states, path)
        loaded = json_to_states(path)
        self.assertEqual(len(loaded), 3)
        self.assertTrue(loaded[-1].done)
        self.assertEqual(loaded[-1].final_path, ["A", "B", "C"])
        self.assertEqual(loaded[1].improved_vertex, "B")
        self.assertTrue(loaded[1].improved)
        # Проверка бесконечности
        states_inf = [AlgorithmState(dist={"A": float('inf'), "B": 5.0}, visited=set(), parent={})]
        path2 = os.path.join(self.tmpdir.name, "states_inf.json")
        states_to_json(states_inf, path2)
        loaded2 = json_to_states(path2)
        self.assertEqual(loaded2[0].dist["A"], float('inf'))