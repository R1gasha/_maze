# tests/test_maze_generator.py
import pytest
from pathlib import Path
from models.maze_generator import MazeGenerator
from tests.helpers import is_perfect, has_valid_borders
from models.maze_model import Maze


# ---- 1. Размеры ----

@pytest.mark.parametrize("rows,cols", [
    (1, 1), (1, 5), (5, 1), (2, 2), (4, 4), (10, 10), (50, 50),
])
def test_generated_maze_has_correct_dimensions(rows, cols):
    maze = MazeGenerator.generate_eller(rows, cols)
    assert maze.rows == rows
    assert maze.cols == cols
    assert len(maze.right_walls) == rows
    assert len(maze.bottom_walls) == rows
    for r in range(rows):
        assert len(maze.right_walls[r]) == cols
        assert len(maze.bottom_walls[r]) == cols


# ---- 2. Внешняя граница ----

@pytest.mark.parametrize("rows,cols", [(1, 1), (2, 3), (5, 5), (10, 7)])
def test_borders_are_walls(rows, cols):
    maze = MazeGenerator.generate_eller(rows, cols)
    assert has_valid_borders(maze)


# ---- 3. Идеальность ----

@pytest.mark.parametrize("rows,cols", [
    (1, 1), (1, 5), (5, 1), (2, 2), (3, 3), (4, 4), (5, 5), (10, 10),
])
def test_maze_is_perfect(rows, cols):
    """Связность + ровно V-1 проходов = дерево."""
    maze = MazeGenerator.generate_eller(rows, cols)
    assert is_perfect(maze), f"Лабиринт {rows}×{cols} не идеален"


# ---- 4. Разные seed дают разные лабиринты (обычно) ----

def test_different_runs_produce_different_mazes():
    mazes = {MazeGenerator.generate_eller(10, 10).right_walls.__repr__()
             for _ in range(5)}
    assert len(mazes) > 1, "Все лабиринты одинаковые — random не работает"


# ---- 5. Детерминизм при фиксированном seed ----

def test_deterministic_with_seed():
    a = MazeGenerator.generate_eller(10, 10, seed=42)
    b = MazeGenerator.generate_eller(10, 10, seed=42)
    assert a.right_walls == b.right_walls
    assert a.bottom_walls == b.bottom_walls


# ---- 6. Валидация параметров ----

@pytest.mark.parametrize("rows,cols", [
    (0, 10), (10, 0), (-1, 5), (5, -1), (51, 10), (10, 51), (100, 100),
])
def test_invalid_size_raises(rows, cols):
    with pytest.raises(ValueError):
        MazeGenerator.generate_eller(rows, cols)


# ---- 7. Round-trip с файлом ----
def test_round_trip_with_file(tmp_path):
    maze = MazeGenerator.generate_eller(8, 8, seed=42)

    path = MazeGenerator.make_file(maze, output_dir=tmp_path)
    assert Path(path).exists()
    assert Path(path).parent == tmp_path

    loaded = Maze.from_file(path)
    assert loaded.rows == maze.rows
    assert loaded.cols == maze.cols
    assert loaded.right_walls == maze.right_walls
    assert loaded.bottom_walls == maze.bottom_walls