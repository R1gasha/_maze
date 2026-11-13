from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt
from models.maze_model import Maze


class MazeWidget(QWidget):
    FIELD_SIZE = 500
    WALL_THICKNESS = 2

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(self.FIELD_SIZE, self.FIELD_SIZE)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)
        self._maze: Maze | None = None
        self._solution: list[tuple[int, int]] | None = None   # ← только путь

    def set_maze(self, maze: Maze | None) -> None:
        self._maze = maze
        self._solution = None        # новый лабиринт — старый путь невалиден
        self.update()                # ← обязательно

    def set_solution(self, path: list[tuple[int, int]] | None) -> None:
        self._solution = path
        self.update()                # ← обязательно

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
            painter.fillRect(self.rect(), QColor("white"))

            if self._maze is not None:
                self._draw_border(painter)
                self._draw_maze(painter)
                self._draw_solution(painter)     # ← поверх стен
            else:
                self._draw_border(painter)
        finally:
            painter.end()

    def _cell_center(self, row: int, col: int) -> tuple[float, float]:
        cw = self.FIELD_SIZE / self._maze.cols
        ch = self.FIELD_SIZE / self._maze.rows
        return (col * cw + cw / 2, row * ch + ch / 2)

    def _draw_solution(self, painter: QPainter) -> None:
        if not self._solution:
            return

        # AA только для линии — стены остаются резкими
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        pen = QPen(QColor("red"))
        pen.setWidth(2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)

        centers = [self._cell_center(r, c) for r, c in self._solution]
        for (x1, y1), (x2, y2) in zip(centers, centers[1:]):
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))

        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)

    def _draw_border(self, painter: QPainter) -> None:
        size = self.FIELD_SIZE
        t = self.WALL_THICKNESS
        color = QColor("black")
        painter.fillRect(0, 0, size, t, color)
        painter.fillRect(0, size - t, size, t, color)
        painter.fillRect(0, 0, t, size, color)
        painter.fillRect(size - t, 0, t, size, color)

    def _draw_maze(self, painter: QPainter) -> None:
        m = self._maze
        size = self.FIELD_SIZE
        t = self.WALL_THICKNESS
        color = QColor("black")

        xs = [round(c * size / m.cols) for c in range(m.cols + 1)]
        ys = [round(r * size / m.rows) for r in range(m.rows + 1)]

        for r in range(m.rows):
            for c in range(m.cols):
                if c < m.cols - 1 and m.right_walls[r][c]:
                    x = xs[c + 1]
                    painter.fillRect(x - t + 1, ys[r], t, ys[r + 1] - ys[r], color)

                if r < m.rows - 1 and m.bottom_walls[r][c]:
                    y = ys[r + 1]
                    painter.fillRect(xs[c], y - t + 1, xs[c + 1] - xs[c], t, color)