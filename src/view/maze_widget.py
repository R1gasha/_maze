from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import Qt
from models.maze_model import Maze


class MazeWidget(QWidget):
    FIELD_SIZE = 500
    WALL_THICKNESS = 2

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(self.FIELD_SIZE, self.FIELD_SIZE)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)
        self._maze = None

    def set_maze(self, maze: Maze):
        if maze is not None:
            self._maze = maze

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        painter.fillRect(self.rect(), QColor("white"))

        if self._maze is not None:
            self._draw_border(painter)
            self._draw_maze(painter)
        else:
            self._draw_border(painter)

        painter.end()

    def _draw_border(self, painter: QPainter) -> None:
        size = self.FIELD_SIZE
        t = self.WALL_THICKNESS
        color = QColor("black")

        painter.fillRect(0, 0, size, t, color)              # верх
        painter.fillRect(0, size - t, size, t, color)       # низ
        painter.fillRect(0, 0, t, size, color)              # лево
        painter.fillRect(size - t, 0, t, size, color)       # право

    def _draw_maze(self, painter: QPainter) -> None:
        m = self._maze
        size = self.FIELD_SIZE
        t = self.WALL_THICKNESS
        color = QColor("black")

        xs = [round(c * size / m.cols) for c in range(m.cols + 1)]
        ys = [round(r * size / m.rows) for r in range(m.rows + 1)]

            # 2. Внутренние стены
        for r in range(m.rows):
            for c in range(m.cols):
                # вертикальная стена справа от (r, c)
                if c < m.cols - 1 and m.right_walls[r][c]:
                    x = xs[c + 1]
                    painter.fillRect(
                        x - t + 1, ys[r],
                        t, ys[r + 1] - ys[r],
                        color,
                    )

                # горизонтальная стена снизу от (r, c)
                if r < m.rows - 1 and m.bottom_walls[r][c]:
                    y = ys[r + 1]
                    painter.fillRect(
                        xs[c], y - t + 1,
                        xs[c + 1] - xs[c], t,
                        color,
                    )