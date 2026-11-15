from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QSpinBox, QMessageBox, QFileDialog,
)
from PySide6.QtCore import Qt, Signal

from view.maze_widget import MazeWidget
from models.maze_model import Maze


class MainWindow(QWidget):
    # --- сигналы: «пользователь сделал X» ---
    load_requested     = Signal()
    generate_requested = Signal(int, int)               # rows, cols
    solve_requested    = Signal(int, int, int, int)     # sr, sc, er, ec

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Maze")
        self.maze_widget = MazeWidget(self)
        self._build_ui()
        self._connect_buttons()

    # --- создание виджетов ---
    def _build_ui(self) -> None:
        self.load_btn = QPushButton("Загрузить")
        self.gen_rows = QSpinBox(); self.gen_rows.setRange(1, 50); self.gen_rows.setValue(10)
        self.gen_cols = QSpinBox(); self.gen_cols.setRange(1, 50); self.gen_cols.setValue(10)
        self.gen_btn  = QPushButton("Сгенерировать")

        top = QHBoxLayout()
        top.addWidget(self.load_btn)
        top.addSpacing(20)
        top.addWidget(QLabel("Строк:"))
        top.addWidget(self.gen_rows)
        top.addWidget(QLabel("Столбцов:"))
        top.addWidget(self.gen_cols)
        top.addWidget(self.gen_btn)
        top.addStretch()

        self.start_row = QSpinBox(); self.start_col = QSpinBox()
        self.end_row   = QSpinBox(); self.end_col   = QSpinBox()
        for sb in (self.start_row, self.start_col, self.end_row, self.end_col):
            sb.setRange(0, 0); sb.setEnabled(False)

        self.solve_btn = QPushButton("Построить путь")
        self.solve_btn.setEnabled(False)

        bottom = QHBoxLayout()
        bottom.addWidget(QLabel("Старт: строка"))
        bottom.addWidget(self.start_row)
        bottom.addWidget(QLabel("столбец"))
        bottom.addWidget(self.start_col)
        bottom.addSpacing(20)
        bottom.addWidget(QLabel("Финиш: строка"))
        bottom.addWidget(self.end_row)
        bottom.addWidget(QLabel("столбец"))
        bottom.addWidget(self.end_col)
        bottom.addStretch()
        bottom.addWidget(self.solve_btn)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 40)
        layout.addLayout(top)
        layout.addWidget(self.maze_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(bottom)
        layout.setSizeConstraint(layout.SizeConstraint.SetFixedSize)

    # --- клики → сигналы ---
    def _connect_buttons(self) -> None:
        self.load_btn.clicked.connect(self.load_requested)
        self.gen_btn.clicked.connect(
            lambda: self.generate_requested.emit(
                self.gen_rows.value(), self.gen_cols.value()
            )
        )
        self.solve_btn.clicked.connect(
            lambda: self.solve_requested.emit(
                self.start_row.value(), self.start_col.value(),
                self.end_row.value(),   self.end_col.value(),
            )
        )

    # ---------------------------------------------------------------
    # Публичный API для контроллера — «что показать»
    # ---------------------------------------------------------------
    def set_maze(self, maze: Maze) -> None:
        self.maze_widget.set_maze(maze)
        self._update_solve_ranges(maze.rows, maze.cols)
        self.solve_btn.setEnabled(True)
        self.setWindowTitle(f"Maze — {maze.rows}×{maze.cols}")

    def set_solution(self, path) -> None:
        self.maze_widget.set_solution(path)

    def clear_solution(self) -> None:
        self.maze_widget.set_solution(None)

    def ask_file_path(self) -> str | None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Открыть лабиринт", "datasets/", "Maze (*.txt)"
        )
        return path or None

    def show_error(self, title: str, message: str) -> None:
        QMessageBox.critical(self, title, message)

    def show_info(self, title: str, message: str) -> None:
        QMessageBox.information(self, title, message)

    # --- вспомогательное ---
    def _update_solve_ranges(self, rows: int, cols: int) -> None:
        for sb in (self.start_row, self.end_row):
            sb.setRange(0, rows - 1)
        for sb in (self.start_col, self.end_col):
            sb.setRange(0, cols - 1)
        for sb in (self.start_row, self.start_col, self.end_row, self.end_col):
            sb.setValue(0); sb.setEnabled(True)