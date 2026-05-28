# Graph Algorithm Visualizer (Dijkstra, A*)

## Interactive desktop application for loading weighted undirected graphs, running Dijkstra's and A* algorithms with step-by-step animation, interactive playback control, and export of results.

### Features:
- Load graphs from text files (with or without vertex coordinates) or enter manually in console.
- Two algorithms: classic [Dijkstra](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm) and [A*](https://en.wikipedia.org/wiki/A*_search_algorithm) with Euclidean heuristic.
- Step-by-step animation showing visited vertices, edge relaxation, distance label updates.
- Interactive controls: Play/Pause, step forward/backward buttons and keyboard shortcuts.
- Color legend and adaptive scaling for graphs of any size.
- Export animation to GIF or MP4.
- Save and load algorithm states in JSON format (replay without recomputation).
- Complete test suite (22 tests) for core modules.

### Requirements:
- Python 3.10 or higher
- Dependencies: networkx >= 3.0, matplotlib >= 3.7, Pillow (optional)
- For MP4 export: ffmpeg

### Installation and Usage:
1. Clone the repository:
   ```bash
   git clone https://github.com/yourname/graph-algorithm-visualizer.git
2. Change directory:
   ```
   cd graph-algorithm-visualizer
3. Install the requirements:
   ```
   pip install -r requirements.txt
4. Run:
   ```
   python run.py --start A --end C --file graph_visualiser/data/sample_graph.txt --algo dijkstra --speed 300
   or(!)
   python -m graph_visualiser --start A --end C --file graph_visualiser/data/sample_graph.txt --algo dijkstra --speed 300

### Controls:
- Space: Play/Pause
- Right/Left arrows: next/previous step
- Esc: close window

### Graph File Format:
Sections VERTICES and EDGES. Vertex line: ID [X Y] (coordinates optional for Dijkstra).

**Example with coordinates**:
VERTICES

A 0 0\
B 200 0\
...

EDGES\
A B 10\
...

*Comments (#) and blank lines ignored. Edge weights must be positive.*

### Usage Examples:
- A* with coordinates: python run.py --start A --end C --file graph_visualiser/data/sample_graph.txt --algo astar --speed 200
- Save to GIF: python run.py ... --export animation.gif
- Save states to JSON: python run.py ... --save-states states.json
- Load states: python run.py --load-states states.json --file ... --algo dijkstra
- Manual input: omit --file and follow prompts.

### Detailed Usage:
Launching the program opens a matplotlib window. The animation starts paused; click "Play" or press Space to begin automatic playback. Use the "Forward" and "Back" buttons or left/right arrow keys to manually step through the algorithm states. The graph display updates in real time:
- Gray vertices are unvisited.
- Teal vertices have been extracted from the priority queue (final distance determined).
- The bright yellow vertex is currently being processed.
- The dashed blue line indicates the edge currently being considered for relaxation.
- If relaxation improves the distance, the edge turns solid orange-red and the distance label under the neighbor vertex turns green.
- When the algorithm completes, the shortest path (if found) is highlighted with thick green edges and orange vertices. If no path exists, a red message appears.
- The legend in the upper left explains all colors.
For large graphs, markers and fonts automatically shrink to avoid clutter.
Exporting to GIF requires Pillow; MP4 requires ffmpeg. When saving states to JSON, the current algorithm state sequence is stored and can be reloaded later with --load-states (the original graph file must still be provided for visualization).

### Testing:
pytest graph_visualiser/tests/\
  or:\
  python -m pytest graph_visualiser/tests/

### Project Structure:
graph-algorithm-visualizer/\
├── run.py.\
├── requirements.txt\
├── README.txt\
└── graph_visualiser/\
    ├── __init__.py\
    ├── __main__.py\
    ├── main.py\
    ├── config.py\
    ├── core/\
    ├── io/\
    ├── viz/\
    ├── utils/\
    ├── data/\
    └── tests/

## License: [MIT](https://github.com/AshtonPL1/graph-algorithm-visualizer/blob/master/LICENSE).

---

# Визуализатор алгоритмов поиска кратчайшего пути (Дейкстра, A*)

## Интерактивное приложение для загрузки взвешенных неориентированных графов, запуска алгоритмов Дейкстры и A* с пошаговой анимацией, интерактивным управлением и экспортом результатов.

### Возможности:
- Загрузка графов из текстовых файлов (с координатами или без) или ручной ввод.
- Алгоритмы [Дейкстры](https://ru.wikipedia.org/wiki/Алгоритм_Дейкстры) и [A*](https://ru.wikipedia.org/wiki/A*) с эвклидовой эвристикой.
- Пошаговая анимация с подсветкой вершин, релаксации рёбер, изменением меток расстояний.
- Кнопки Play/Pause, перемотка, клавиатурные сокращения.
- Цветовая легенда и адаптивное масштабирование.
- Экспорт анимации в GIF или MP4.
- Сохранение и загрузка состояний в JSON.
- 22 модульных теста.

### Требования:
- Python 3.10 или выше
- Зависимости: networkx, matplotlib, Pillow (опционально)
- Для MP4: ffmpeg

### Установка и запуск:
1. Клонирование репозитория:
   ```
   git clone https://github.com/yourname/graph-algorithm-visualizer.git
2. Смените директорию:
   ```
   cd graph-algorithm-visualizer
3. Установите зависимости:
   ```
   pip install -r requirements.txt
4. Запуск:
   ```
   python run.py --start A --end C --file graph_visualiser/data/sample_graph.txt --algo dijkstra --speed 300
   или(!)
   python -m graph_visualiser --start A --end C --file graph_visualiser/data/sample_graph.txt --algo dijkstra --speed 300

### Управление:
- Пробел: Play/Pause
- Стрелки вправо/влево: следующий/предыдущий шаг
- Esc: закрыть окно

### Формат файла графа:
*Секции VERTICES и EDGES. Вершины: ID [X Y] (координаты необязательны для Дейкстры). Комментарии # и пустые строки игнорируются. Веса рёбер положительные.*

### Примеры:
- A* с координатами: python run.py --start A --end C --file ... --algo astar --speed 200
- Сохранение в GIF: python run.py ... --export animation.gif
- Сохранение состояний в JSON: python run.py ... --save-states states.json
- Загрузка состояний: python run.py --load-states states.json --file ... --algo dijkstra
- Ручной ввод: не указывать --file, следовать инструкциям в консоли.

### Подробное использование:
После запуска открывается окно matplotlib. Анимация изначально на паузе; нажмите "Play" или Пробел для автоматического воспроизведения. Кнопки "Forward"/"Back" и стрелки влево/вправо позволяют перемещаться по шагам вручную. Отображение графа обновляется в реальном времени:
- Серые вершины — не посещённые.
- Бирюзовые — извлечённые из очереди с приоритетом (окончательное расстояние определено).
- Ярко-жёлтая вершина — текущая обрабатываемая.
- Синяя пунктирная линия — ребро, рассматриваемое на данном шаге релаксации.
- Если релаксация улучшает расстояние, ребро становится сплошным оранжево-красным, а метка расстояния под соседней вершиной зеленеет.
- По завершении алгоритма кратчайший путь (если найден) выделяется толстыми зелёными линиями и оранжевыми вершинами. Если путь не существует, появляется красное сообщение.
- Легенда в левом верхнем углу поясняет все цвета.
Для больших графов маркеры и шрифты автоматически уменьшаются, чтобы избежать нагромождения.
Экспорт в GIF требует Pillow; MP4 – ffmpeg. При сохранении состояний в JSON последовательность шагов алгоритма сохраняется и может быть позже загружена с помощью --load-states (для визуализации по-прежнему нужен исходный файл графа).

### Тестирование:
pytest graph_visualiser/tests/\
  или:\
  python -m pytest graph_visualiser/tests/

### Структура проекта:
graph-algorithm-visualizer/\
├── run.py\
├── requirements.txt\
├── README.txt\
└── graph_visualiser/\
    ├── __init__.py\
    ├── __main__.py\
    ├── main.py\
    ├── config.py\
    ├── core/\
    ├── io/\
    ├── viz/\
    ├── utils/\
    ├── data/\
    └── tests/

## Лицензия: [MIT](https://github.com/AshtonPL1/graph-algorithm-visualizer/blob/master/LICENSE).
