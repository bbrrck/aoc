import numpy as np

with open("input.txt", "r") as f:
    lines = f.read().strip("\n").split("\n")

n = len(lines)

EMPTY_SPACE = "."
ROLLING_ROCK = "O"
STATIC_ROCK = "#"
EMPTY_SPACE_NUM = 0
ROLLING_ROCK_NUM = 1
STATIC_ROCK_NUM = 2


def str_to_num(x):
    if x == ROLLING_ROCK:
        return ROLLING_ROCK_NUM
    if x == STATIC_ROCK:
        return STATIC_ROCK_NUM
    return EMPTY_SPACE_NUM


def num_to_str(rolling, static):
    s = ""
    for i in range(n):
        if i in static:
            s += STATIC_ROCK
        elif i in rolling:
            s += ROLLING_ROCK
        else:
            s += EMPTY_SPACE
    return s


def tilt_north(mat):
    for x in range(n):
        y0 = -1
        for y, rock in enumerate(mat[:, x]):
            if rock == ROLLING_ROCK:
                y0 += 1
                mat[y0, x], mat[y, x] = mat[y, x], mat[y0, x]
            elif rock == STATIC_ROCK:
                y0 = y


def get_load(mat):
    rows, _ = np.where(mat == "O")
    return (n - rows).sum()


def cycle(mat):
    # north
    tilt_north(mat)
    # west
    mat = mat.T
    tilt_north(mat)
    mat = mat.T
    # south
    mat = np.flipud(mat)
    tilt_north(mat)
    mat = np.flipud(mat)
    # east
    mat = np.fliplr(mat).T
    tilt_north(mat)
    mat = np.fliplr(mat.T)


#### Part 1
M = np.array([[x for x in line] for line in lines])
tilt_north(M)
answer_1 = get_load(M)
print(answer_1)

#### Part 2
N_CYCLES = 1_000_000_000

hash_table = {}
matrices = {}

M = np.array([[x for x in line] for line in lines])
h = "".join(
    M.reshape(
        -1,
    ).tolist()
)
hash_table[h] = 0
matrices[0] = M.copy()

cycle_len = -1
for iter in range(1_000):
    cycle(M)
    h = "".join(
        M.reshape(
            -1,
        ).tolist()
    )
    if h in hash_table:
        first = hash_table[h]
        # print(f"Found repetition at {iter=}, {first=}")
        check = np.all(matrices[first] == M)
        # print(f"Check if matrices are equal: {check = }")
        cycle_len = iter - first
        break
    hash_table[h] = iter
    matrices[iter] = M.copy()

final = (N_CYCLES - first) % cycle_len + first - 1
# print(f"#{final} is the final matrix after {N_CYCLES} cycles")
answer_2 = get_load(matrices[final])
print(answer_2)
