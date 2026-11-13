from models.maze_model import Maze
from collections import deque

class MazeSolver:
    @staticmethod
    def solve(maze: Maze, start, end) -> list[tuple[int, int]] | None:
        right_walls = maze.right_walls
        bottom_walls = maze.bottom_walls
        cols = maze.cols
        rows = maze.rows
        came_from = MazeSolver._bfs(start, end, cols, rows, right_walls, bottom_walls)
        solve = MazeSolver._get_path(start, end, came_from)
        return solve

    @staticmethod
    def _bfs(start_point, end_point, cols, rows, matrix_r, matrix_b):

        visit_points = set()
        came_from = dict()

        if start_point == end_point:
            return {start_point: end_point}

        if came_from is None:
            came_from = dict()

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
            route.append(parent[route[-1]])
        return route[::-1]