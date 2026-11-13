import sys
from PySide6.QtWidgets import QApplication
from view.main_window import MainWindow
from models.maze_model import Maze


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())