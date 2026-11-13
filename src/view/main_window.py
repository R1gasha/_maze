from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt

from view.maze_widget import MazeWidget
from models.maze_model import Maze


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Maze")

        self.maze_widget = MazeWidget(self)

        maze = Maze.from_file('datasets/test_eller.txt')
        self.maze_widget.set_maze(maze)

        # try:
        #     maze = Maze.from_file('datasets/test_1.txt')
        #     self.maze_widget.set_maze(maze)
        # except ValueError as e:
        #     print(e)


        layout = QVBoxLayout(self)
        # Отступы вокруг лабиринта, в пикселях
        layout.setContentsMargins(40, 40, 40, 40)
        # AlignCenter — виджет по центру, не растягивается
        layout.addWidget(self.maze_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        # Окно подстраивается под содержимое + отступы = 500 + 40 + 40 = 580
        layout.setSizeConstraint(layout.SizeConstraint.SetFixedSize)