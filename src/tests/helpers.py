# tests/helpers.py
from collections import deque
from models.maze_model import Maze


def bfs_reachable(maze: Maze, start: tuple[int, int]) -> set[tuple[int, int]]:
    """Множество клеток, достижимых из start по проходам (BFS)."""
    visited = {start}
    queue = deque([start])
    while queue:
        r, c = queue.popleft()
        for nr, nc in _neighbors(maze, r, c):
            if (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc))
    return visited


def _neighbors(maze: Maze, r: int, c: int) -> list[tuple[int, int]]:
    result = []
    if r + 1 < maze.rows and not maze.bottom_walls[r][c]:
        result.append((r + 1, c))
    if r > 0 and not maze.bottom_walls[r - 1][c]:
        result.append((r - 1, c))
    if c + 1 < maze.cols and not maze.right_walls[r][c]:
        result.append((r, c + 1))
    if c > 0 and not maze.right_walls[r][c - 1]:
        result.append((r, c - 1))
    return result


def count_passages(maze: Maze) -> int:
    """Число внутренних проходов (нулей) во всех матрицах стен."""
    n = 0
    for r in range(maze.rows):
        for c in range(maze.cols - 1):
            if not maze.right_walls[r][c]:
                n += 1
    for r in range(maze.rows - 1):
        for c in range(maze.cols):
            if not maze.bottom_walls[r][c]:
                n += 1
    return n


def is_perfect(maze: Maze) -> bool:
    """Идеальный = связный + ровно V-1 проходов (дерево)."""
    if not bfs_reachable(maze, (0, 0)) == {
        (r, c) for r in range(maze.rows) for c in range(maze.cols)
    }:
        return False
    return count_passages(maze) == maze.rows * maze.cols - 1


def has_valid_borders(maze: Maze) -> bool:
    """Внешняя граница: все стены на месте."""
    for r in range(maze.rows):
        if maze.right_walls[r][maze.cols - 1] != 1:
            return False
    for c in range(maze.cols):
        if maze.bottom_walls[maze.rows - 1][c] != 1:
            return False
    return True