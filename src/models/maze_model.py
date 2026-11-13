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

        cols, rows = lines[0][0], lines[0][1]

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

                


# maze = Maze.from_file('datasets/test_1.txt')


    # @classmethod
    # def from_file(cls, path: str):

    #     with open(path, 'r') as file:
    #         first_line = file.readline().split()
    #         lines = [line.strip() for line in file]
    #         print(lines)
    #         if len(first_line) != 2:
    #             print('Invalid size')
    #             return

    #         #set size
    #         rows, cols = int(first_line[0]), int(first_line[1])

    #         if (rows <= 0 and rows > 50) or (cols <= 0 and cols > 50):
    #             raise ValueError

    #         right_walls = [[0 for _ in range(cols)] for _ in range(rows)]
    #         bottom_walls = [[0 for _ in range(cols)] for _ in range(rows)]

    #         try:
    #             next_line_right = list(map(int, file.readline().split()))
    #             i = 0
    #             while next_line_right != []:
    #                 right_walls[i] = next_line_right
    #                 i += 1
    #                 next_line_right = list(map(int, file.readline().split()))

    #             next_line_bottom = list(map(int, file.readline().split()))
    #             i = 0
    #             while next_line_bottom:
    #                 bottom_walls[i] = next_line_bottom
    #                 i += 1
    #                 next_line_bottom = list(map(int, file.readline().split()))
    #         except ValueError as e:
    #             raise ValueError(e)

    #         actual_total = rows * cols

    #         count_right = sum(len(row) for row in right_walls)
    #         count_bottom = sum(len(row) for row in bottom_walls)

    #         if actual_total != count_right or actual_total != count_bottom:
    #             raise ValueError("Invalid size")

    #         return cls(rows, cols, right_walls, bottom_walls)