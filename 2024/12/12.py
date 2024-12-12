import sys
from pathlib import Path

filename = Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else sys.argv[1]

with open(filename) as f:
    data = f.read()  # noqa: F841

# ------------------------------------------------

size = len(data.splitlines())
grid = data.replace("\n", "")


def idx_to_pos(idx: int) -> tuple[int, int]:
    return (idx // size, idx % size)


def pos_to_idx(r: int, c: int) -> int:
    if r < 0 or r >= size or c < 0 or c >= size:
        return None
    return r * size + c


def _g(r: int, c: int, default: str | None = None):
    i = pos_to_idx(r, c)
    if i is None:
        return default
    return grid[i]


def count_corners(i):
    x = grid[i]
    r, c = idx_to_pos(i)
    # 4-neighborhood: top-down-left-right
    x_t = _g(r - 1, c, ".")
    x_d = _g(r + 1, c, ".")
    x_l = _g(r, c - 1, ".")
    x_r = _g(r, c + 1, ".")
    # 8-neighborhood: diagonals
    x_tl = _g(r - 1, c - 1, x)
    x_tr = _g(r - 1, c + 1, x)
    x_bl = _g(r + 1, c - 1, x)
    x_br = _g(r + 1, c + 1, x)
    n = 0
    # Outer corners
    n += int(x_t != x and x_l != x)
    n += int(x_t != x and x_r != x)
    n += int(x_d != x and x_l != x)
    n += int(x_d != x and x_r != x)
    # Inner corners
    n += int(x_t == x and x_l == x and x_tl != x)
    n += int(x_t == x and x_r == x and x_tr != x)
    n += int(x_d == x and x_l == x and x_bl != x)
    n += int(x_d == x and x_r == x and x_br != x)
    return n


answer_1 = 0
answer_2 = 0
unvisited = set(range(size * size))
regions = []
while len(unvisited) > 0:
    # Start a new region
    i_start = unvisited.pop()
    region = []
    queue = [i_start]
    area = 1
    perimeter = 0
    while queue:
        # Pop the next cell from queue
        i0 = queue.pop()
        region.append(i0)
        x0 = grid[i0]
        r0, c0 = idx_to_pos(i0)
        # Visit all cells in 4-neighborhood
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r1, c1 = r0 + dr, c0 + dc
            i1 = pos_to_idx(r1, c1)
            x1 = _g(r1, c1)
            if r1 < 0 or r1 >= size or c1 < 0 or c1 >= size or x0 != x1:
                # We have reached the border of the region
                perimeter += 1
                continue
            if i1 not in unvisited:
                # We have reached a cell in this region that has already been visited
                continue
            # Add this cell to the current region
            queue.append(i1)
            unvisited.remove(i1)
            area += 1
    # Number of sides is the same as number of corners
    n_sides = sum(count_corners(i) for i in region)
    answer_1 += area * perimeter
    answer_2 += area * n_sides
    regions.append(region)
print(answer_1)
print(answer_2)
