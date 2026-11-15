from models.maze_model import Maze
from models.maze_generator import MazeGenerator
from models.maze_solver import MazeSolver
from view.main_window import MainWindow


class MazeController:
    def __init__(self, view) -> None:
        self._view: MainWindow = view
        self._maze: Maze | None = None

        # подписываемся на сигналы view
        view.load_requested.connect(self._on_load)
        view.generate_requested.connect(self._on_generate)
        view.solve_requested.connect(self._on_solve)

    # ---------------------------------------------------------------
    # Обработчики сигналов — вся бизнес-логика здесь
    # ---------------------------------------------------------------
    def _on_load(self) -> None:
        path = self._view.ask_file_path()
        if path is None:
            return
        try:
            maze = Maze.from_file(path)
        except (ValueError, OSError) as exc:
            self._view.show_error("Ошибка загрузки", str(exc))
            return
        self._apply_maze(maze)

    def _on_generate(self, rows: int, cols: int) -> None:
        try:
            maze = MazeGenerator.generate_eller(rows, cols)
            path = MazeGenerator.make_file(maze)
            maze = Maze.from_file(path)                 # проверка round-trip
        except (ValueError, OSError) as exc:
            self._view.show_error("Ошибка генерации", str(exc))
            return
        self._apply_maze(maze)

    def _on_solve(self, sr: int, sc: int, er: int, ec: int) -> None:
        if self._maze is None:
            return
        start, end = (sr, sc), (er, ec)

        if start == end:
            self._view.clear_solution()
            self._view.show_info("Решение", "Старт и финиш совпадают")
            return

        path = MazeSolver.solve(self._maze, start, end)
        if path is None:
            self._view.clear_solution()
            self._view.show_info("Решение", "Пути не существует")
            return

        self._view.set_solution(path)

    # --- общее ---
    def _apply_maze(self, maze: Maze) -> None:
        self._maze = maze
        self._view.set_maze(maze)