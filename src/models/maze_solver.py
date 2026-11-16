from models.maze_model import Maze
from collections import deque

class MazeSolver:
    @staticmethod
    def solve(maze: Maze, start, end) -> list[tuple[int, int]] | None:
        if not isinstance(start, tuple) or not isinstance(end, tuple):
            raise ValueError("Not valid data")
        if len(start) != 2 or len(end) != 2:
            raise ValueError("Not valid data")

        cols = maze.cols
        rows = maze.rows
        
        if start[0] < 0 or start[0] >= rows or start[1] < 0 or start[1] >= cols:
            raise IndexError("Output index range")
        if end[0] < 0 or end[0] >= rows or end[1] < 0 or end[1] >= cols:
            raise IndexError("Output index range")
        right_walls = maze.right_walls
        bottom_walls = maze.bottom_walls

        came_from = MazeSolver._bfs(start, end, cols, rows, right_walls, bottom_walls)
        route = MazeSolver._get_path(start, end, came_from)
        return route

    @staticmethod
    def _bfs(start_point, end_point, cols, rows, matrix_r, matrix_b):

        visit_points = set()
        came_from = dict()

        if start_point == end_point:
            return {start_point: end_point}

        coord_i = start_point[0]
        coord_j = start_point[1]
        
        deque_ = deque()
        deque_.append(start_point)

        while deque_:
            point = deque_.popleft()

            coord_i = point[0]
            coord_j = point[1]

            if coord_i + 1 < rows and matrix_b[coord_i][coord_j] != 1:
                if (coord_i + 1, coord_j) not in visit_points:
                    visit_points.add((coord_i + 1, coord_j))
                    came_from[((coord_i + 1, coord_j))] = (coord_i, coord_j)
                    deque_.append((coord_i + 1, coord_j))
            if coord_i != 0 and matrix_b[coord_i - 1][coord_j] != 1:
                if (coord_i - 1, coord_j) not in visit_points:
                    visit_points.add((coord_i - 1, coord_j))
                    came_from[((coord_i - 1, coord_j))] = (coord_i, coord_j) 
                    deque_.append((coord_i - 1, coord_j))
            if coord_j + 1 < cols and matrix_r[coord_i][coord_j] != 1: 
                if (coord_i, coord_j + 1) not in visit_points:
                    visit_points.add((coord_i, coord_j + 1))
                    came_from[((coord_i, coord_j + 1))] = (coord_i, coord_j) 
                    deque_.append((coord_i, coord_j + 1))
            if coord_j != 0 and matrix_r[coord_i][coord_j - 1] != 1:
                if (coord_i, coord_j - 1) not in visit_points:
                    visit_points.add((coord_i, coord_j - 1))
                    came_from[((coord_i, coord_j - 1))] = (coord_i, coord_j) 
                    deque_.append((coord_i, coord_j - 1))

        return came_from if end_point in came_from else None    

    @staticmethod
    def _get_path(start, end, parent):
        if parent is None:
            return None
        route = [end]
        while route[-1] != start:
            p = parent.get(route[-1])
            if p is None:
                return None
            route.append(p)
        return route[::-1]