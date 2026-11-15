import sys
from PySide6.QtWidgets import QApplication

from view.main_window import MainWindow
from controller.maze_controller import MazeController


def main() -> int:
    app = QApplication(sys.argv)

    view = MainWindow()
    controller = MazeController(view)     # ← связка
    view.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())