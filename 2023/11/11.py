from itertools import combinations

import numpy as np

with open("input.txt", "r") as f:
    M = np.array(
        [
            [1 if x == "#" else 0 for x in row]
            for row in f.read().strip("\n").split("\n")
        ]
    )
empty_cols = np.nonzero(M.sum(axis=0) == 0)
empty_rows = np.nonzero(M.sum(axis=1) == 0)
stars_rows, stars_cols = np.where(M == 1)
answer_1, answer_2 = 0, 0
for (y1, x1), (y2, x2) in combinations(zip(stars_rows, stars_cols), 2):
    x_min, x_max = (x1, x2) if x1 < x2 else (x2, x1)
    y_min, y_max = (y1, y2) if y1 < y2 else (y2, y1)
    n_empty_cols = ((empty_cols > x_min) & (empty_cols < x_max)).sum()
    n_empty_rows = ((empty_rows > y_min) & (empty_rows < y_max)).sum()
    dist = np.abs(x2 - x1) + np.abs(y2 - y1)
    answer_1 += dist + (n_empty_cols + n_empty_rows)
    answer_2 += dist + (n_empty_cols + n_empty_rows) * 999_999
print(answer_1)
print(answer_2)
