import pytest
from models.maze_model import Maze

def _write_maze_file(tmp_path, content: str) -> str:
    path = tmp_path / "maze.txt"
    path.write_text(content, encoding="utf-8")
    return str(path)


# ============================================================
# HAPPY PATH
# ============================================================

def test_from_file_valid_4x4(tmp_path):
    """Эталонный maze4.txt из задания."""
    path = _write_maze_file(tmp_path, (
        "4 4\n"
        "0 0 0 1\n"
        "1 0 1 1\n"
        "0 1 0 1\n"
        "0 0 0 1\n"
        "\n"
        "1 0 1 0\n"
        "0 0 1 0\n"
        "1 1 0 1\n"
        "1 1 1 1\n"
    ))
    maze = Maze.from_file(path)
    assert maze.rows == 4
    assert maze.cols == 4
    assert maze.right_walls == [
        [0, 0, 0, 1],
        [1, 0, 1, 1],
        [0, 1, 0, 1],
        [0, 0, 0, 1],
    ]
    assert maze.bottom_walls == [
        [1, 0, 1, 0],
        [0, 0, 1, 0],
        [1, 1, 0, 1],
        [1, 1, 1, 1],
    ]


@pytest.mark.parametrize("rows,cols", [(1, 1), (1, 5), (5, 1), (50, 50)])
def test_from_file_valid_boundary_sizes(tmp_path, rows, cols):
    """Граничные размеры: 1×1, 1×N, N×1, 50×50."""
    content = f"{rows} {cols}\n"
    content += (" ".join(["0"] * cols) + "\n") * rows
    content += "\n"
    content += (" ".join(["0"] * cols) + "\n") * rows
    maze = Maze.from_file(_write_maze_file(tmp_path, content))
    assert maze.rows == rows
    assert maze.cols == cols
    assert len(maze.right_walls) == rows
    assert len(maze.bottom_walls) == rows
    for r in range(rows):
        assert len(maze.right_walls[r]) == cols
        assert len(maze.bottom_walls[r]) == cols


def test_from_file_ignores_extra_whitespace(tmp_path):
    """Пробелы, табы, пустые строки — не ломают парсинг."""
    path = _write_maze_file(tmp_path, (
        "  4   4  \n"
        "\n"
        "0 0 0 1\n\n"
        "1 0 1 1\n"
        "0 1 0 1\n"
        "0 0 0 1\n"
        "\n\n"
        "1 0 1 0\n"
        "0 0 1 0\n"
        "1 1 0 1\n"
        "1 1 1 1\n"
        "\n"
    ))
    maze = Maze.from_file(path)
    assert maze.rows == 4
    assert maze.cols == 4


# ============================================================
# ФАЙЛ
# ============================================================

def test_from_file_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        Maze.from_file(str(tmp_path / "nonexistent.txt"))


def test_from_file_empty_file_raises(tmp_path):
    with pytest.raises(ValueError):
        Maze.from_file(_write_maze_file(tmp_path, ""))


def test_from_file_whitespace_only_raises(tmp_path):
    with pytest.raises(ValueError):
        Maze.from_file(_write_maze_file(tmp_path, "\n\n   \n\t\n"))


# ============================================================
# ПЕРВАЯ СТРОКА (РАЗМЕРЫ)
# ============================================================

@pytest.mark.parametrize("first_line", ["4", "4 4 4", "a b", "4.5 4", "4 x"])
def test_from_file_invalid_first_line(tmp_path, first_line):
    path = _write_maze_file(tmp_path, f"{first_line}\n0 0 0 1\n")
    with pytest.raises(ValueError):
        Maze.from_file(path)


@pytest.mark.parametrize("rows,cols", [
    (-1, 4), (4, -1), (-1, -1),
    (51, 4), (4, 51), (51, 51), (100, 100),
])
def test_from_file_size_out_of_range_raises(tmp_path, rows, cols):
    path = _write_maze_file(tmp_path, f"{rows} {cols}\n")
    with pytest.raises(ValueError):
        Maze.from_file(path)


@pytest.mark.parametrize("rows,cols", [(0, 0), (0, 4), (4, 0)])
def test_from_file_zero_size_raises(tmp_path, rows, cols):
    path = _write_maze_file(tmp_path, f"{rows} {cols}\n")
    with pytest.raises(ValueError):
        Maze.from_file(path)


# ============================================================
# НЕЧИСЛОВЫЕ ЗНАЧЕНИЯ
# ============================================================

@pytest.mark.parametrize("bad", ["abc", "1.5", "#", "0x1", "1a"])
def test_from_file_non_numeric_raises(tmp_path, bad):
    content = (
        "2 2\n"
        f"0 {bad}\n"
        "1 0\n"
        "\n"
        "1 0\n"
        "0 1\n"
    )
    with pytest.raises(ValueError):
        Maze.from_file(_write_maze_file(tmp_path, content))


# ============================================================
# КОЛИЧЕСТВО СТРОК
# ============================================================

def test_from_file_too_few_lines_raises(tmp_path):
    path = _write_maze_file(tmp_path, (
        "4 4\n"
        "0 0 0 1\n"
        "1 0 1 1\n"
    ))
    with pytest.raises(ValueError):
        Maze.from_file(path)


def test_from_file_too_many_lines_raises(tmp_path):
    path = _write_maze_file(tmp_path, (
        "2 2\n"
        "0 1\n"
        "1 0\n"
        "\n"
        "1 0\n"
        "0 1\n"
        "0 1\n"
    ))
    with pytest.raises(ValueError):
        Maze.from_file(path)


# ============================================================
# ДЛИНА СТРОКИ МАТРИЦЫ
# ============================================================

def test_from_file_row_too_short_raises(tmp_path):
    """right_walls[1] содержит 3 значения вместо 4."""
    path = _write_maze_file(tmp_path, (
        "4 4\n"
        "0 0 0 1\n"
        "1 0 1\n"
        "0 1 0 1\n"
        "0 0 0 1\n"
        "\n"
        "1 0 1 0\n"
        "0 0 1 0\n"
        "1 1 0 1\n"
        "1 1 1 1\n"
    ))
    with pytest.raises(ValueError):
        Maze.from_file(path)


def test_from_file_row_too_long_raises(tmp_path):
    """right_walls[0] содержит 5 значений вместо 4."""
    path = _write_maze_file(tmp_path, (
        "4 4\n"
        "0 0 0 1 1\n"
        "1 0 1 1\n"
        "0 1 0 1\n"
        "0 0 0 1\n"
        "\n"
        "1 0 1 0\n"
        "0 0 1 0\n"
        "1 1 0 1\n"
        "1 1 1 1\n"
    ))
    with pytest.raises(ValueError):
        Maze.from_file(path)


# ============================================================
# ЗНАЧЕНИЯ НЕ 0/1
# ============================================================

@pytest.mark.parametrize("bad_value", [2, -1, 99, 255, 10])
def test_from_file_non_binary_value_raises(tmp_path, bad_value):
    path = _write_maze_file(tmp_path, (
        "2 2\n"
        f"0 {bad_value}\n"
        "1 0\n"
        "\n"
        "1 0\n"
        "0 1\n"
    ))
    with pytest.raises(ValueError):
        Maze.from_file(path)


@pytest.mark.parametrize("bad_value", [2, -1, 99])
def test_from_file_non_binary_in_bottom_walls_raises(tmp_path, bad_value):
    """Проверка нижней матрицы — отдельно от верхней."""
    path = _write_maze_file(tmp_path, (
        "2 2\n"
        "0 1\n"
        "1 0\n"
        "\n"
        f"1 {bad_value}\n"
        "0 1\n"
    ))
    with pytest.raises(ValueError):
        Maze.from_file(path)


# ============================================================
# ROUND-TRIP (если есть make_file — используйте его)
# ============================================================

def test_from_file_round_trip_with_make_file(tmp_path):
    """make_file → from_file → тот же лабиринт."""
    from models.maze_generator import MazeGenerator
    maze = MazeGenerator.generate_eller(8, 8, seed=42)
    path = MazeGenerator.make_file(maze, output_dir=tmp_path)
    loaded = Maze.from_file(path)
    assert loaded.rows == maze.rows
    assert loaded.cols == maze.cols
    assert loaded.right_walls == maze.right_walls
    assert loaded.bottom_walls == maze.bottom_walls