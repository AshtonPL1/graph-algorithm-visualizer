"""
Animator class that creates a matplotlib window with interactive controls,
legend, adaptive scaling, and plays the algorithm steps.

Класс аниматора, создающий окно matplotlib с интерактивными элементами управления,
легендой, адаптивным масштабированием и воспроизводящий шаги алгоритма.
"""

import os
from pathlib import Path
from typing import List, Dict, Tuple, Optional

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
from matplotlib.patches import Patch
import networkx as nx

from ..core.state import AlgorithmState
from ..utils.colors import (
    VERTEX_DEFAULT, VERTEX_VISITED, VERTEX_CURRENT, VERTEX_PATH,
    EDGE_DEFAULT, EDGE_RELAX, EDGE_PATH, EDGE_RELAX_IMPROVED,
    TEXT_DARK, PATH_MISSING_COLOR,
    EDGE_DEFAULT_WIDTH, EDGE_RELAX_WIDTH, EDGE_PATH_WIDTH, EDGE_RELAX_IMPROVED_WIDTH,
    VERTEX_MARKER_SIZE, FONT_SIZE_ID, FONT_SIZE_DIST, LABEL_OFFSET, DIST_IMPROVED,
)
from ..utils.settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_DPI, EXPORT_DPI, EXPORT_FPS,
)


class GraphAnimator:
    """
    Handles drawing of graph states, interactive controls, legend, adaptive scaling.

    Управляет отрисовкой состояний графа, интерактивными элементами, легендой, адаптивным масштабом.
    """
    def __init__(
        self,
        G: nx.Graph,
        states: List[AlgorithmState],
        speed_ms: int,
        algo_name: str,
        has_coordinates: bool,
    ):
        self.G = G
        self.states = states
        self.speed = speed_ms
        self.algo_name = algo_name
        self.has_coordinates = has_coordinates
        self.current_frame = 0
        self.paused = True
        self.running = True

        # Prepare positions
        if has_coordinates:
            self.pos = nx.get_node_attributes(G, 'pos')
        else:
            self.pos = nx.spring_layout(G, seed=42)

        # Adaptive scaling based on number of vertices
        # Адаптивное масштабирование в зависимости от числа вершин
        n = len(G.nodes)
        if n > 100:
            self.marker_size = VERTEX_MARKER_SIZE / 3
            self.font_id = FONT_SIZE_ID - 3
            self.font_dist = FONT_SIZE_DIST - 2
            self.label_offset = LABEL_OFFSET / 2
            self.edge_width_factor = 0.5
        elif n > 30:
            self.marker_size = VERTEX_MARKER_SIZE / 1.5
            self.font_id = FONT_SIZE_ID - 1
            self.font_dist = FONT_SIZE_DIST
            self.label_offset = LABEL_OFFSET * 0.8
            self.edge_width_factor = 0.8
        else:
            self.marker_size = VERTEX_MARKER_SIZE
            self.font_id = FONT_SIZE_ID
            self.font_dist = FONT_SIZE_DIST
            self.label_offset = LABEL_OFFSET
            self.edge_width_factor = 1.0

        # Create figure
        self.fig = plt.figure(figsize=(WINDOW_WIDTH, WINDOW_HEIGHT), dpi=WINDOW_DPI)
        self.fig.subplots_adjust(top=0.85, bottom=0.15)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.set_aspect('equal')
        self.ax.axis('off')

        # Legend patches (will be drawn once or per frame – better on first frame)
        self._legend_drawn = False

        self._setup_widgets()
        self._connect_keyboard()

        title = f"Graph Algorithm Visualizer — {algo_name}"
        self.ax.set_title(title, fontsize=14, pad=60)

    def _setup_widgets(self):
        btn_width = 0.08
        btn_height = 0.05
        self.btn_play_pause_ax = self.fig.add_axes([0.3, 0.02, btn_width, btn_height])
        self.btn_play_pause = Button(self.btn_play_pause_ax, 'Play')
        self.btn_play_pause.on_clicked(self._on_play_pause)

        self.btn_forward_ax = self.fig.add_axes([0.45, 0.02, btn_width, btn_height])
        self.btn_forward = Button(self.btn_forward_ax, 'Forward')
        self.btn_forward.on_clicked(self._on_step_forward)

        self.btn_backward_ax = self.fig.add_axes([0.6, 0.02, btn_width, btn_height])
        self.btn_backward = Button(self.btn_backward_ax, 'Back')
        self.btn_backward.on_clicked(self._on_step_backward)

    def _connect_keyboard(self):
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _on_key_press(self, event):
        if event.key == ' ':
            self._on_play_pause(None)
        elif event.key == 'right':
            self._on_step_forward(None)
        elif event.key == 'left':
            self._on_step_backward(None)
        elif event.key == 'escape':
            plt.close(self.fig)

    def _on_play_pause(self, event):
        self.paused = not self.paused
        self.btn_play_pause.label.set_text('Pause' if not self.paused else 'Play')

    def _on_step_forward(self, event):
        if self.current_frame < len(self.states) - 1:
            self.current_frame += 1
            self._draw_frame(self.states[self.current_frame], self.current_frame)
            self.fig.canvas.draw_idle()

    def _on_step_backward(self, event):
        if self.current_frame > 0:
            self.current_frame -= 1
            self._draw_frame(self.states[self.current_frame], self.current_frame)
            self.fig.canvas.draw_idle()

    def _draw_legend(self):
        """Draw legend explaining colors and styles (only once)."""
        legend_elements = [
            Patch(facecolor=VERTEX_DEFAULT, edgecolor='black', label='Unvisited'),
            Patch(facecolor=VERTEX_VISITED, edgecolor='black', label='Visited'),
            Patch(facecolor=VERTEX_CURRENT, edgecolor='black', label='Current'),
            Patch(facecolor=VERTEX_PATH, edgecolor='black', label='Path vertex'),
            plt.Line2D([0], [0], color=EDGE_PATH, linewidth=EDGE_PATH_WIDTH, label='Final path edge'),
            plt.Line2D([0], [0], color=EDGE_RELAX, linewidth=EDGE_RELAX_WIDTH, linestyle='--', label='Relaxation (no improve)'),
            plt.Line2D([0], [0], color=EDGE_RELAX_IMPROVED, linewidth=EDGE_RELAX_IMPROVED_WIDTH, label='Relaxation (improved)'),
            plt.Line2D([0], [0], color=EDGE_DEFAULT, linewidth=EDGE_DEFAULT_WIDTH, label='Default edge'),
        ]
        self.ax.legend(handles=legend_elements, loc='upper left', fontsize=8, framealpha=0.7)

    def _draw_frame(self, state: AlgorithmState, frame_idx: int):
        self.ax.clear()
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        title = f"Graph Algorithm Visualizer — {self.algo_name} (Step {frame_idx+1}/{len(self.states)})"
        self.ax.set_title(title, fontsize=14, pad=60)

        # Draw legend once
        if not self._legend_drawn:
            self._draw_legend()
            self._legend_drawn = True  # unfortunately clear() removes legend, so we redraw every frame.
            # Actually clear() clears everything, so legend must be redrawn. We'll redraw each frame.
        self._draw_legend()  # redraw after clear

        # Determine final path edge set
        final_path_edges = set()
        if state.final_path and len(state.final_path) > 1:
            path = state.final_path
            for i in range(len(path)-1):
                u, v = path[i], path[i+1]
                final_path_edges.add(frozenset((u, v)))

        # Scale edge widths by factor
        ew_default = EDGE_DEFAULT_WIDTH * self.edge_width_factor
        ew_relax = EDGE_RELAX_WIDTH * self.edge_width_factor
        ew_path = EDGE_PATH_WIDTH * self.edge_width_factor
        ew_improved = EDGE_RELAX_IMPROVED_WIDTH * self.edge_width_factor

        for u, v, edge_data in self.G.edges(data=True):
            p1 = self.pos[u]
            p2 = self.pos[v]
            if final_path_edges and frozenset((u, v)) in final_path_edges:
                color = EDGE_PATH
                width = ew_path
                style = '-'
            elif state.relax_edge and frozenset((u, v)) == frozenset(state.relax_edge):
                if state.improved:
                    color = EDGE_RELAX_IMPROVED
                    width = ew_improved
                    style = '-'
                else:
                    color = EDGE_RELAX
                    width = ew_relax
                    style = '--'
            else:
                color = EDGE_DEFAULT
                width = ew_default
                style = '-'

            self.ax.plot(
                [p1[0], p2[0]], [p1[1], p2[1]],
                color=color, linewidth=width, linestyle=style, alpha=0.8, zorder=1
            )

            # Edge weight label (scale font)
            mid_x = (p1[0] + p2[0]) / 2
            mid_y = (p1[1] + p2[1]) / 2
            weight = edge_data.get('weight', 0.0)
            self.ax.text(
                mid_x, mid_y, f"{weight:.2f}",
                fontsize=self.font_dist * 0.7, color=TEXT_DARK,
                ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.8),
                zorder=3
            )

        # Draw vertices
        for v in self.G.nodes:
            x, y = self.pos[v]
            if state.final_path and v in state.final_path:
                color = VERTEX_PATH
            elif v == state.current_vertex:
                color = VERTEX_CURRENT
            elif v in state.visited:
                color = VERTEX_VISITED
            else:
                color = VERTEX_DEFAULT

            self.ax.scatter(
                x, y, s=self.marker_size, c=color, edgecolors='black',
                linewidth=1.5, zorder=2
            )

            # ID label
            self.ax.text(
                x, y + self.label_offset, str(v),
                fontsize=self.font_id, ha='center', va='bottom', fontweight='bold', zorder=4
            )

            # Distance label
            d = state.dist.get(v, float('inf'))
            d_str = f"{d:.2f}" if d != float('inf') else "∞"

            if self.algo_name == "A*" and state.f_values is not None:
                f_val = state.f_values.get(v, float('inf'))
                f_str = f"{f_val:.2f}" if f_val != float('inf') else "∞"
                label = f"{d_str} | {f_str}"
            else:
                label = d_str

            dist_color = TEXT_DARK
            if state.improved_vertex == v:
                dist_color = DIST_IMPROVED

            self.ax.text(
                x, y - self.label_offset, label,
                fontsize=self.font_dist, ha='center', va='top', color=dist_color, zorder=4
            )

        # Auto-fit axes with padding
        xs = [p[0] for p in self.pos.values()]
        ys = [p[1] for p in self.pos.values()]
        if xs and ys:
            x_min, x_max = min(xs), max(xs)
            y_min, y_max = min(ys), max(ys)
            x_margin = (x_max - x_min) * 0.1 if x_max != x_min else 10
            y_margin = (y_max - y_min) * 0.1 if y_max != y_min else 10
            self.ax.set_xlim(x_min - x_margin, x_max + x_margin)
            self.ax.set_ylim(y_min - y_margin, y_max + y_margin)

        if state.done and not state.final_path:
            cx = (min(xs) + max(xs)) / 2 if xs else 0
            cy = (min(ys) + max(ys)) / 2 if ys else 0
            self.ax.text(
                cx, cy, "Path not found",
                fontsize=14, color=PATH_MISSING_COLOR,
                ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.9),
                zorder=10
            )

    def animate(self) -> None:
        self._draw_frame(self.states[0], 0)
        self.paused = True
        self.btn_play_pause.label.set_text('Play')

        timer = self.fig.canvas.new_timer(interval=self.speed)
        timer.add_callback(self._timer_tick)
        timer.start()

        plt.show()
        plt.close(self.fig)

    def _timer_tick(self):
        if not self.running:
            return
        if not self.paused:
            if self.current_frame < len(self.states) - 1:
                self.current_frame += 1
                self._draw_frame(self.states[self.current_frame], self.current_frame)
                self.fig.canvas.draw_idle()
            else:
                self.paused = True
                self.btn_play_pause.label.set_text('Play')
                self.fig.canvas.draw_idle()

    def save_animation(self, filepath: str) -> None:
        filepath = Path(filepath)
        ext = filepath.suffix.lower()
        writer = None
        if ext == '.gif':
            try:
                import PIL
                writer = 'pillow'
            except ImportError:
                raise ImportError("Pillow is required to save GIF. Install 'pip install pillow'.")
        elif ext == '.mp4':
            try:
                writer = 'ffmpeg'
            except ImportError:
                raise ImportError("ffmpeg is required to save MP4. Install ffmpeg.")
        else:
            raise ValueError(f"Unsupported export format '{ext}'. Use .gif or .mp4.")

        fig, ax = plt.subplots(figsize=(WINDOW_WIDTH, WINDOW_HEIGHT), dpi=EXPORT_DPI)
        fig.subplots_adjust(top=0.85)
        ax.set_aspect('equal')
        ax.axis('off')

        export_animator = GraphAnimator(self.G, self.states, self.speed, self.algo_name, self.has_coordinates)
        export_animator.fig = fig
        export_animator.ax = ax
        export_animator.pos = self.pos

        def update_export(frame):
            ax.clear()
            export_animator._draw_frame(self.states[frame], frame)

        ani = animation.FuncAnimation(
            fig, update_export, frames=len(self.states),
            interval=self.speed, repeat=False, blit=False
        )

        ani.save(str(filepath), writer=writer, dpi=EXPORT_DPI, fps=EXPORT_FPS)
        plt.close(fig)
        print(f"Animation saved to {filepath.resolve()}")