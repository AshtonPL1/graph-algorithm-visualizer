"""
Tests for graph file loader.

Тесты для загрузчика графов из файла.
"""

import unittest
import tempfile
import os
from graph_visualiser.io.graph_reader import load_graph_from_file
from graph_visualiser.utils.exceptions import FileFormatError, FileNotFoundErrorGraph


class TestGraphReader(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmpdir.cleanup()

    def _create_file(self, content):
        path = os.path.join(self.tmpdir.name, "graph.txt")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return path

    def test_valid_with_coords(self):
        content = """VERTICES
A 0 0
B 10 10
C 20 0
EDGES
A B 5.0
B C 3.0
"""
        path = self._create_file(content)
        cfg = load_graph_from_file(path)
        self.assertTrue(cfg.has_coordinates)
        self.assertEqual(len(cfg.graph.nodes), 3)
        self.assertEqual(len(cfg.graph.edges), 2)

    def test_valid_without_coords(self):
        content = """VERTICES
A
B
C
EDGES
A B 5.0
B C 3.0
"""
        path = self._create_file(content)
        cfg = load_graph_from_file(path)
        self.assertFalse(cfg.has_coordinates)
        self.assertEqual(len(cfg.graph.nodes), 3)

    def test_inconsistent_coords(self):
        content = """VERTICES
A 0 0
B
C
EDGES
A B 5.0
"""
        path = self._create_file(content)
        with self.assertRaises(FileFormatError):
            load_graph_from_file(path)

    def test_duplicate_vertex(self):
        content = """VERTICES
A 0 0
A 1 1
EDGES
"""
        path = self._create_file(content)
        with self.assertRaises(FileFormatError):
            load_graph_from_file(path)

    def test_edge_nonexistent_vertex(self):
        content = """VERTICES
A 0 0
B 1 1
EDGES
A C 5.0
"""
        path = self._create_file(content)
        with self.assertRaises(FileFormatError):
            load_graph_from_file(path)

    def test_loop_edge(self):
        content = """VERTICES
A 0 0
EDGES
A A 5.0
"""
        path = self._create_file(content)
        with self.assertRaises(FileFormatError):
            load_graph_from_file(path)

    def test_negative_weight(self):
        content = """VERTICES
A 0 0
B 1 1
EDGES
A B -2.0
"""
        path = self._create_file(content)
        with self.assertRaises(FileFormatError):
            load_graph_from_file(path)

    def test_missing_sections(self):
        content = "A 0 0"
        path = self._create_file(content)
        with self.assertRaises(FileFormatError):
            load_graph_from_file(path)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundErrorGraph):
            load_graph_from_file("nonexistent.txt")