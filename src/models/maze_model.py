from dataclasses import dataclass
from typing import List

@dataclass
class Maze:
    rows: int
    cols: int
    right_walls: List[List[int]]
    bottom_walls: List[List[int]]

    @classmethod
    def from_file(cls, path: str):

        with open(path, 'r') as file:
            lines = [line.strip() for line in file]

        try:
            lines = [list(map(int, line.split())) for line in lines if line]
        except:
            raise ValueError("Invalid char")

        if len(lines[0]) != 2:
            raise ValueError("Invalid set size matrix")

        rows, cols = lines[0][0], lines[0][1]

        if cols < 0 or cols > 50 or rows < 0 or rows > 50:
            raise ValueError("Invalid set size matrix")

        except_lines = 1 + 2 * rows

        if len(lines) != except_lines:
            raise ValueError("Invalid rows matrix")

        right_walls = [[0 for _ in range(cols)] for _ in range(rows)]
        bottom_walls = [[0 for _ in range(cols)] for _ in range(rows)]

        for i in range(rows):
            right_walls[i] = lines[1 + i]

        for i in range(rows):
            bottom_walls[i] = lines[i + rows + 1]

        return cls(rows, cols, right_walls, bottom_walls)

    @staticmethod
    def _read_matrix():
        pass