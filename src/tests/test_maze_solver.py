# tests/test_maze_solver.py
import pytest
from models.maze_solver import MazeSolver
from tests.helpers import bfs_reachable


# ---- 1. Валидация входа ----

@pytest.mark.parametrize("start,end", [
    (42, (0, 0)),                 # start не кортеж
    ((0, 0), 42),                 # end не кортеж
    ((0, 0, 0), (0, 1)),          # start из 3
    ((0, 0), (0, 1, 2)),          # end из 3
    ("00", (0, 1)),               # start — строка
    (None, (0, 0)),               # start — None
])
def test_solve_rejects_invalid_types(small_maze, start, end):
    with pytest.raises(ValueError):
        MazeSolver.solve(small_maze, start, end)


@pytest.mark.parametrize("start,end", [
    ((-1, 0), (0, 0)),            # start < 0
    ((0, -1), (0, 0)),
    ((4, 0), (0, 0)),             # start == rows
    ((0, 4), (0, 0)),             # start == cols
    ((0, 0), (-1, 0)),            # end < 0
    ((0, 0), (4, 0)),
    ((0, 0), (0, 4)),
])
def test_solve_rejects_out_of_bounds(small_maze, start, end):
    with pytest.raises(IndexError):
        MazeSolver.solve(small_maze, start, end)


@pytest.mark.parametrize("start,end", [
    ((0, 0), (0, 1)),             # нули — валидны
    ((0, 0), (0, 0)),             # start == end
    ((3, 3), (0, 0)),             # последняя клетка
    ((0, 3), (3, 0)),
])
def test_solve_accepts_valid_coordinates(small_maze, start, end):
    """(0, *) и (rows-1, cols-1) — валидны, не должны падать."""
    # не должно бросить
    MazeSolver.solve(small_maze, start, end)


# ---- 2. Корректность пути ----

def test_path_starts_and_ends_correctly(small_maze):
    start, end = (0, 0), (3, 3)
    path = MazeSolver.solve(small_maze, start, end)
    assert path is not None
    assert path[0] == start
    assert path[-1] == end


def test_path_cells_are_adjacent_and_not_wall_blocked(small_maze):
    path = MazeSolver.solve(small_maze, (0, 0), (3, 3))
    assert path is not None
    for (r1, c1), (r2, c2) in zip(path, path[1:]):
        assert abs(r1 - r2) + abs(c1 - c2) == 1, f"Не соседние: {(r1,c1)} → {(r2,c2)}"
        # проверить, что нет стены между ними
        if r2 == r1 + 1:
            assert small_maze.bottom_walls[r1][c1] == 0
        elif r2 == r1 - 1:
            assert small_maze.bottom_walls[r2][c1] == 0
        elif c2 == c1 + 1:
            assert small_maze.right_walls[r1][c1] == 0
        elif c2 == c1 - 1:
            assert small_maze.right_walls[r1][c2] == 0


def test_path_is_shortest(small_maze):
    """BFS → длина пути = манхэттенское расстояние в идеальном лабиринте."""
    # в идеальном лабиринте путь единственный, но проверяем длину
    path = MazeSolver.solve(small_maze, (0, 0), (3, 3))
    assert path is not None
    # длина = число клеток - 1 = число шагов
    # если путь единственный, BFS даёт его, и он же кратчайший
    assert len(path) >= abs(3 - 0) + abs(3 - 0) + 1


# ---- 3. Start == end ----

def test_start_equals_end(small_maze):
    path = MazeSolver.solve(small_maze, (2, 2), (2, 2))
    # по контракту _bfs: {start: start} → [start]
    assert path == [(2, 2)]


# ---- 4. Нет пути (несвязный лабиринт) ----

def test_no_path_returns_none(disconnected_maze):
    """(0,0) изолирована, до (3,3) не дойти."""
    path = MazeSolver.solve(disconnected_maze, (0, 0), (3, 3))
    assert path is None


# ---- 5. Полный проход по всем клеткам ----

@pytest.mark.parametrize("start", [(0, 0), (1, 2), (2, 1), (3, 3)])
def test_solve_from_any_cell(small_maze, start):
    """Из любой точки достижима любая — идеальный лабиринт."""
    path = MazeSolver.solve(small_maze, start, (0, 0) if start != (0, 0) else (3, 3))
    assert path is not None