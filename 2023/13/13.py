import numpy as np

with open("input.txt", "r") as f:
    puzzles = f.read().strip("\n").split("\n\n")

matrices = [
    np.array([[1 if x == "#" else 0 for x in line] for line in puzzle.split("\n")])
    for puzzle in puzzles
]


#### Part 1
def row_reflection(M):
    n_reflected_rows = 0
    for i in range(1, M.shape[0]):
        M0 = M[:i, :]
        M1 = M[i:, :]
        k = min(M0.shape[0], M1.shape[0])
        M0 = M[i - k : i, :]
        M1 = M[i : i + k, :]
        M1_flipped = np.flip(M1, axis=0)
        if np.all(M0 == M1_flipped):
            n_reflected_rows = i
    return n_reflected_rows


def col_reflection(M):
    n_reflected_cols = 0
    for i in range(1, M.shape[1]):
        M0 = M[:, :i]
        M1 = M[:, i:]
        k = min(M0.shape[1], M1.shape[1])
        M0 = M[:, i - k : i]
        M1 = M[:, i : i + k]
        M1_flipped = np.flip(M1, axis=1)
        if np.all(M0 == M1_flipped):
            n_reflected_cols = i
    return n_reflected_cols


answer_1 = 0
for midx, M in enumerate(matrices):
    r = row_reflection(M)
    c = col_reflection(M)
    answer_1 += 100 * r + c
print(answer_1)


#### Part 2
def row_reflection_2(M):
    n_reflected_rows = 0
    for i in range(1, M.shape[0]):
        M0 = M[:i, :]
        M1 = M[i:, :]
        k = min(M0.shape[0], M1.shape[0])
        M0 = M[i - k : i, :]
        M1 = M[i : i + k, :]
        M1_flipped = np.flip(M1, axis=0)
        if np.sum(M0 != M1_flipped) == 1:
            n_reflected_rows = i
    return n_reflected_rows


def col_reflection_2(M):
    n_reflected_cols = 0
    for i in range(1, M.shape[1]):
        M0 = M[:, :i]
        M1 = M[:, i:]
        k = min(M0.shape[1], M1.shape[1])
        M0 = M[:, i - k : i]
        M1 = M[:, i : i + k]
        M1_flipped = np.flip(M1, axis=1)
        if np.sum(M0 != M1_flipped) == 1:
            n_reflected_cols = i
    return n_reflected_cols


answer_2 = 0
for midx, M in enumerate(matrices):
    r = row_reflection_2(M)
    c = col_reflection_2(M)
    answer_2 += 100 * r + c
print(answer_2)
