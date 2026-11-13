import random
cols, rows = 7, 7

set_matrix = [[-1 for j in range(cols)] for i in range(rows)]
right_walls = [[1 for j in range(cols)] for i in range(rows)]
bottom_walls = [[0 for j in range(cols)] for i in range(rows)]
count = 1

i = 0

for index_ in range(cols):
    set_matrix[i][index_] = count
    count += 1

while i < (rows - 1):

    # right walls
    for j in range(cols - 1):
        result = random.randint(0, 1)
        if result == 1:
            right_walls[i][j] = 1
        elif set_matrix[i][j] == set_matrix[i][j + 1]:
            right_walls[i][j] = 1                  # принудительно, 3.2
        else:
            right_walls[i][j] = 0                  # 3.3 — слияние
            actual_set = set_matrix[i][j]
            zamena_set = set_matrix[i][j + 1]
            for m in range(rows):
                for n in range(cols):
                    if set_matrix[m][n] == zamena_set:
                        set_matrix[m][n] = actual_set

    for j in range(cols):
        result = random.randint(0, 1)
        if result == 0:
            continue
        elif result == 1:
            actual_set = set_matrix[i][j]
            count_bottom_walls = 0
            count_bottom_walls = sum(
                1 for n in range(cols)
                if set_matrix[i][n] == actual_set and bottom_walls[i][n] == 0
            )
            if count_bottom_walls > 1:
                bottom_walls[i][j] = 1         

    i += 1

    #set_matrix[i] = set_matrix[i - 1]
    set_matrix[i] = [set_matrix[i - 1][index] for index in range(cols)]
    right_walls[i] = [right_walls[i - 1][index] for index in range(cols)]
    bottom_walls[i] = [bottom_walls[i - 1][index] for index in range(cols)]

    for k in range(cols):
        right_walls[i][k] = 0

    for k in range(cols):
        if bottom_walls[i][k] == 1:
            set_matrix[i][k] = 0
        bottom_walls[i][k] = 0

    for k in range(cols):
        if set_matrix[i][k] == 0:
            set_matrix[i][k] = count
            count += 1


for k in range(cols - 1):
    if set_matrix[i][k] == set_matrix[i][k + 1]:
        right_walls[i][k] = 1
    else:
        right_walls[i][k] = 0
        old = set_matrix[i][k + 1]
        new = set_matrix[i][k]
        for m in range(rows):            # ← все строки
            for n in range(cols):        # ← все столбцы
                if set_matrix[m][n] == old:
                    set_matrix[m][n] = new


for k in range(cols):
    bottom_walls[i][k] = 1

for k in range(cols):
    right_walls[k][i] = 1  


print(set_matrix)
print(right_walls)
print(bottom_walls)

with open('datasets/test_eller.txt', 'w') as file:
    file.write(f'{rows} {cols}\n' )
    for index in range(cols):
        file.write(' '.join(map(str, right_walls[index])) + '\n')
    file.write('\n')
    for index in range(cols):
        file.write(' '.join(map(str, bottom_walls[index])) + '\n')