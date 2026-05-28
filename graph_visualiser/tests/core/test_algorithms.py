"""
Tests for Dijkstra and A* step-by-step generators.

Тесты для пошаговых генераторов Дейкстры и A*.
"""

import unittest
import networkx as nx
from graph_visualiser.core.algorithms import DijkstraAlgorithm, AStarAlgorithm
from graph_visualiser.core.state import AlgorithmState


class TestDijkstra(unittest.TestCase):
    def setUp(self):
        # Простой треугольник с центром
        self.G = nx.Graph()
        self.G.add_node("A", pos=(0, 0))
        self.G.add_node("B", pos=(200, 0))
        self.G.add_node("C", pos=(100, 173.205))
        self.G.add_node("D", pos=(100, 57.735))
        self.G.add_edge("A", "B", weight=10)
        self.G.add_edge("B", "C", weight=10)
        self.G.add_edge("C", "A", weight=10)
        self.G.add_edge("A", "D", weight=5.77)
        self.G.add_edge("B", "D", weight=5.77)
        self.G.add_edge("C", "D", weight=5.77)

    def test_path_found(self):
        algo = DijkstraAlgorithm(self.G)
        states = list(algo.run("A", "C"))
        self.assertTrue(len(states) > 0)
        last = states[-1]
        self.assertTrue(last.done)
        self.assertIsNotNone(last.final_path)
        self.assertEqual(last.final_path[0], "A")
        self.assertEqual(last.final_path[-1], "C")
        # Кратчайший путь A-C напрямую: вес 10.0
        self.assertAlmostEqual(last.dist["C"], 10.0, delta=0.01)
        self.assertEqual(last.final_path, ["A", "C"])

    def test_no_path(self):
        # Добавим изолированную компоненту
        self.G.add_node("E", pos=(400, 400))
        algo = DijkstraAlgorithm(self.G)
        states = list(algo.run("A", "E"))
        last = states[-1]
        self.assertTrue(last.done)
        self.assertIsNone(last.final_path)
        self.assertEqual(last.dist["E"], float('inf'))

    def test_start_equals_target(self):
        algo = DijkstraAlgorithm(self.G)
        states = list(algo.run("A", "A"))
        last = states[-1]
        self.assertTrue(last.done)
        self.assertEqual(last.final_path, ["A"])
        self.assertEqual(last.dist["A"], 0.0)


class TestAStar(unittest.TestCase):
    def setUp(self):
        self.G = nx.Graph()
        self.G.add_node("S", pos=(0, 0))
        self.G.add_node("G", pos=(10, 0))
        self.G.add_node("M", pos=(5, 5))
        self.G.add_edge("S", "G", weight=15)
        self.G.add_edge("S", "M", weight=7)
        self.G.add_edge("M", "G", weight=7)

    def test_path_found(self):
        algo = AStarAlgorithm(self.G)   # используем A*, не Dijkstra
        states = list(algo.run("S", "G"))  # вершины из setUp: S, G
        self.assertTrue(len(states) > 0)
        last = states[-1]
        self.assertTrue(last.done)
        self.assertIsNotNone(last.final_path)
        # Путь S->M->G весом 14.0
        self.assertAlmostEqual(last.dist["G"], 14.0, delta=0.01)
        self.assertEqual(last.final_path, ["S", "M", "G"])

    def test_no_coordinates_raises(self):
        G_no_pos = nx.Graph()
        G_no_pos.add_node("A")
        G_no_pos.add_node("B")
        G_no_pos.add_edge("A", "B", weight=5)
        with self.assertRaises(ValueError):
            AStarAlgorithm(G_no_pos)