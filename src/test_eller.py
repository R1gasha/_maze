import random

import random


def generate_eller(rows: int, cols: int, seed: int | None = None):
    if rows < 1 or cols < 1:
        raise ValueError(f"Размер должен быть ≥ 1, получено {rows}×{cols}")

    rng = random.Random(seed)

    right_walls  = [[1] * cols for _ in range(rows)]   # стены — убираем
    bottom_walls = [[0] * cols for _ in range(rows)]   # проходы — ставим
    sets = [0] * cols                                  # одна строка id

    count = 1

    # --- Первая строка: выдать id каждой клетке (один раз) ---
    for c in range(cols):
        sets[c] = count
        count += 1

    i = 0
    while i < rows - 1:
        # --- Горизонтальный проход ---
        for j in range(cols - 1):
            result = rng.randint(0, 1)
            if result == 1:
                right_walls[i][j] = 1
            elif sets[j] == sets[j + 1]:
                right_walls[i][j] = 1                  # 3.2 — принудительно
            else:
                right_walls[i][j] = 0                  # 3.3 — слияние
                _merge(sets, sets[j + 1], sets[j])

        # --- Вертикальный проход ---
        set_sizes = {}
        for c in range(cols):
            s = sets[c]
            set_sizes[s] = set_sizes.get(s, 0) + 1

        set_open = dict(set_sizes)             # ← ВСЕ ОТКРЫТЫ с самого начала
        has_bottom = [False] * cols

        for j in range(cols):
            s = sets[j]
            result = rng.randint(0, 1)
            if result == 1:
                if set_open[s] - 1 >= 1:
                    bottom_walls[i][j] = 1
                    set_open[s] -= 1
                    continue
            bottom_walls[i][j] = 0
            has_bottom[j] = True

        # --- Переход к следующей строке: обновить sets на месте ---
        i += 1
        for c in range(cols):
            if not has_bottom[c]:
                sets[c] = count                        # новый id
                count += 1
            # else: sets[c] наследует id — не трогаем

    # --- Последняя строка (i = rows - 1) ---
    for k in range(cols - 1):
        if sets[k] == sets[k + 1]:
            right_walls[i][k] = 1
        else:
            right_walls[i][k] = 0
            _merge(sets, sets[k + 1], sets[k])

    # --- Границы ---
    for k in range(cols):
        bottom_walls[i][k] = 1
    for r in range(rows):
        right_walls[r][cols - 1] = 1

    return right_walls, bottom_walls


def _merge(sets, old_id, new_id):
    """Слияние в одной строке: все old_id → new_id."""
    for k in range(len(sets)):
        if sets[k] == old_id:
            sets[k] = new_id

right_walls, bottom_walls = generate_eller(7,7)

print(right_walls)
print(bottom_walls)

with open('datasets/test_eller.txt', 'w') as file:
    file.write(f'{7} {7}\n' )
    for index in range(7):
        file.write(' '.join(map(str, right_walls[index])) + '\n')
    file.write('\n')
    for index in range(7):
        file.write(' '.join(map(str, bottom_walls[index])) + '\n')