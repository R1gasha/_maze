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

        with open(path, 'r', encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]

        if not lines:
            raise ValueError("Empty file")

        try:
            lines = [list(map(int, line.split())) for line in lines if line]
        except:
            raise ValueError("Invalid char")

        if len(lines[0]) != 2:
            raise ValueError("Invalid set size matrix")

        rows, cols = lines[0]

        if not (1 <= rows <= 50 and 1 <= cols <= 50):
            raise ValueError("Invalid set size matrix")

        except_lines = 1 + 2 * rows

        if len(lines) != except_lines:
            raise ValueError("Invalid rows matrix")

        right_walls = []
        bottom_walls = []
        for i in range(rows):
            row = lines[1 + i]
            if len(row) != cols:                                    # ← длина строки
                raise ValueError("Invalid file")
            if any(v not in (0, 1) for v in row):                   # ← 0/1
                raise ValueError("Invalid file")
            right_walls.append(row)

        for i in range(rows):
            row = lines[1 + rows + i]
            if len(row) != cols:
                raise ValueError("Invalid file")
            if any(v not in (0, 1) for v in row):
                raise ValueError("Invalid file")
            bottom_walls.append(row)

        return cls(rows, cols, right_walls, bottom_walls)

    @staticmethod
    def _read_matrix():
        pass