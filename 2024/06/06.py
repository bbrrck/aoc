import re
import sys
from pathlib import Path

from tqdm import tqdm

filename = Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else sys.argv[1]

with open(filename) as f:
    data = f.read()  # noqa: F841


def idx_to_pos(idx):
    return (idx // size, idx % size)


def pos_to_idx(r, c):
    return r * size + c


TOP, DOWN, LEFT, RIGHT = "^", "v", "<", ">"

size = len(data.splitlines())
grid = data.replace("\n", "")
dir = TOP
i_start = grid.index(dir)

# print(data)
# print(size)
# print(i0)
# print(r0, c0)

#### Part 1

r0, c0 = idx_to_pos(i_start)
grid_visited = grid
max_iter = 10 * size * size
n_visited = 0
while True:
    if n_visited > max_iter:
        raise RuntimeError
    i0 = pos_to_idx(r0, c0)
    grid_visited = grid_visited[:i0] + "X" + grid_visited[i0 + 1 :]
    n_visited += 1
    # Get position of next cell
    if dir == TOP:
        r1, c1 = r0 - 1, c0
    elif dir == DOWN:
        r1, c1 = r0 + 1, c0
    elif dir == LEFT:
        r1, c1 = r0, c0 - 1
    elif dir == RIGHT:
        r1, c1 = r0, c0 + 1
    # Stop if we are outside the grid
    if r1 < 0 or r1 >= size or c1 < 0 or c1 >= size:
        break
    # If the next cell is a block, turn right 90 degrees
    if grid[r1 * size + c1] == "#":
        if dir == TOP:
            dir = RIGHT
        elif dir == RIGHT:
            dir = DOWN
        elif dir == DOWN:
            dir = LEFT
        elif dir == LEFT:
            dir = TOP
    # otherwise, move and increase the counter
    else:
        r0, c0 = r1, c1
answer_1 = grid_visited.count("X")
# for r in range(size):
#     print(grid_visited[r * size : (r + 1) * size])
print(answer_1)

# ------------------------------------------------

# Part 2
# - place a new obstacle along the covered path except i_start

# find all occurences of X
obstacles = [m.start() for m in re.finditer("X", grid_visited)]
# remove the starting position
obstacles.remove(i_start)


def is_valid_obstacle(obstacle):
    grid_new = grid[:obstacle] + "#" + grid[obstacle + 1 :]
    r0, c0 = idx_to_pos(i_start)
    dir = TOP
    max_iter = size * size  # this could be refined
    n_iter = 0
    while True:
        if n_iter > max_iter:
            # Guard is caught in a loop
            return True
        n_iter += 1
        # Get position of next cell
        if dir == TOP:
            r1, c1 = r0 - 1, c0
        elif dir == DOWN:
            r1, c1 = r0 + 1, c0
        elif dir == LEFT:
            r1, c1 = r0, c0 - 1
        elif dir == RIGHT:
            r1, c1 = r0, c0 + 1
        # Stop if we are outside the grid
        if r1 < 0 or r1 >= size or c1 < 0 or c1 >= size:
            return False
        # If the next cell is a block, turn right 90 degrees
        if grid_new[r1 * size + c1] == "#":
            if dir == TOP:
                dir = RIGHT
            elif dir == RIGHT:
                dir = DOWN
            elif dir == DOWN:
                dir = LEFT
            elif dir == LEFT:
                dir = TOP
        # otherwise, move and increase the counter
        else:
            r0, c0 = r1, c1


# this is quite slow, but it works
answer_2 = 0
for o in tqdm(obstacles):
    if is_valid_obstacle(o):
        answer_2 += 1
print(answer_2)

# ------------------------------------------------
