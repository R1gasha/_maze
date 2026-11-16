# tests/conftest.py
import pytest
from models.maze_model import Maze


@pytest.fixture
def small_maze() -> Maze:
    """Идеальный 4×4 из примера ТЗ (maze4.txt)."""
    return Maze(
        rows=4, cols=4,
        right_walls=[
            [0, 0, 0, 1],
            [1, 0, 1, 1],
            [0, 1, 0, 1],
            [0, 0, 0, 1],
        ],
        bottom_walls=[
            [1, 0, 1, 0],
            [0, 0, 1, 0],
            [1, 1, 0, 1],
            [1, 1, 1, 1],
        ],
    )


@pytest.fixture
def disconnected_maze() -> Maze:
    """4×4 с изолированной клеткой (0,0) — пути нет."""
    m = Maze(
        rows=4, cols=4,
        right_walls=[[0] * 4 for _ in range(4)],
        bottom_walls=[[0] * 4 for _ in range(4)],
    )
    # Стены вокруг (0,0)
    m.right_walls[0][0] = 1     # справа от (0,0)
    m.bottom_walls[0][0] = 1    # снизу от (0,0)
    return m