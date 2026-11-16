
import random
from datetime import datetime
from models.maze_model import Maze
import os

class MazeGenerator:


    @staticmethod
    def generate_eller(rows: int, cols: int, seed: int | None = None):
        if rows < 1 or cols < 1:
            raise ValueError(f"Size must be >= 1 {rows}×{cols}")

        if rows > 50 or cols > 50:
            raise ValueError(f"Size must be <= 50 {rows}×{cols}")

        rng = random.Random(seed)

        right_walls  = [[1] * cols for _ in range(rows)]   # стены — убираем
        bottom_walls = [[0] * cols for _ in range(rows)]   # проходы — ставим
        sets = [0] * cols                                  # одна строка id

        count = 1

        # --- Первая строка: выдать id каждой клетке (один раз) ---
        for c in range(cols):
            sets[c] = count
            count += 1

        i = 0
        while i < rows - 1:
            # --- Горизонтальный проход ---
            for j in range(cols - 1):
                result = rng.randint(0, 1)
                if result == 1:
                    right_walls[i][j] = 1
                elif sets[j] == sets[j + 1]:
                    right_walls[i][j] = 1                  # 3.2 — принудительно
                else:
                    right_walls[i][j] = 0                  # 3.3 — слияние
                    MazeGenerator._merge(sets, sets[j + 1], sets[j])

            # --- Вертикальный проход ---
            set_sizes = {}
            for c in range(cols):
                s = sets[c]
                set_sizes[s] = set_sizes.get(s, 0) + 1

            set_open = dict(set_sizes)             # ← ВСЕ ОТКРЫТЫ с самого начала
            has_bottom = [False] * cols

            for j in range(cols):
                s = sets[j]
                result = rng.randint(0, 1)
                if result == 1:
                    if set_open[s] - 1 >= 1:
                        bottom_walls[i][j] = 1
                        set_open[s] -= 1
                        continue
                bottom_walls[i][j] = 0
                has_bottom[j] = True

            # update sets
            i += 1
            for c in range(cols):
                if not has_bottom[c]:
                    sets[c] = count
                    count += 1
                # else: sets[c] наследует id — не трогаем

        # last row
        for k in range(cols - 1):
            if sets[k] == sets[k + 1]:
                right_walls[i][k] = 1
            else:
                right_walls[i][k] = 0
                MazeGenerator._merge(sets, sets[k + 1], sets[k])

        # right walls
        for k in range(cols):
            bottom_walls[i][k] = 1
        # bottom walls
        for r in range(rows):
            right_walls[r][cols - 1] = 1

        maze = Maze(rows, cols, right_walls, bottom_walls)
        return maze

    @staticmethod
    def _merge(sets, old_id, new_id):
        """Слияние в одной строке: все old_id → new_id."""
        for k in range(len(sets)):
            if sets[k] == old_id:
                sets[k] = new_id

    @staticmethod
    def make_file(maze: Maze, output_dir: str | None = None) -> str:
        if output_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            output_dir = os.path.join(base_dir, "datasets")
        else:
            output_dir = str(output_dir)

        os.makedirs(output_dir, exist_ok=True)

        file_name = f'maze_eller_{MazeGenerator._timestamp()}.txt'
        path = os.path.join(output_dir, file_name)

        
        with open(path, 'w', encoding="utf-8") as file:
            file.write(f'{maze.rows} {maze.cols}\n' )
            for index in range(maze.rows):
                file.write(' '.join(map(str, maze.right_walls[index])) + '\n')
            file.write('\n')
            for index in range(maze.rows):
                file.write(' '.join(map(str, maze.bottom_walls[index])) + '\n')

        return path

    @staticmethod
    def _timestamp() -> str:
        return datetime.now().strftime('%Y%m%d_%H%M%S_%f')