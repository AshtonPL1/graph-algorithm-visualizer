"""
Custom exceptions for graph operations with exit codes.

Пользовательские исключения для операций с графом с кодами выхода.
"""

class GraphError(Exception):
    """
    Base exception for graph-related errors, carrying an exit code and message.

    Базовое исключение для ошибок, связанных с графом, несущее код выхода и сообщение.
    """
    def __init__(self, message: str, exit_code: int = 1):
        super().__init__(message)
        self.exit_code = exit_code
        self.message = message


class FileFormatError(GraphError):
    """
    Raised when the graph file has invalid syntax or violates constraints.
    exit_code = 3.

    Возникает при неверном синтаксисе или нарушении ограничений в файле графа.
    """
    def __init__(self, message: str, line_number: int = 0):
        full_message = f"Line {line_number}: {message}" if line_number else message
        super().__init__(full_message, exit_code=3)


class FileNotFoundErrorGraph(GraphError):
    """
    Raised when the specified file does not exist. exit_code = 4.

    Возникает, когда указанный файл не существует.
    """
    def __init__(self, filepath: str):
        super().__init__(f"File not found: {filepath}", exit_code=4)


class MissingCoordinatesError(GraphError):
    """
    Raised when A* is requested but vertices lack coordinates. exit_code = 5.

    Возникает, когда запрошен A*, но вершины не имеют координат.
    """
    def __init__(self):
        super().__init__("Algorithm A* requires vertex coordinates.", exit_code=5)


class VertexNotFoundError(GraphError):
    """
    Raised when start or end vertex is missing from the graph. exit_code = 6.

    Возникает, когда стартовая или конечная вершина отсутствует в графе.
    """
    def __init__(self, vertex_id: str):
        super().__init__(f"Vertex '{vertex_id}' not found in the graph.", exit_code=6)