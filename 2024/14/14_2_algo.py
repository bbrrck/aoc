import re
import sys
from pathlib import Path

filename = (
    Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else Path(sys.argv[1])
)

if filename.name == "test.txt":
    wide = 11
    tall = 7
elif filename.name == "input.txt":
    wide = 101
    tall = 103
else:
    raise RuntimeError(f"Unknown input file: {filename}")

with open(filename) as f:
    robots = [
        list(map(int, robot))
        for robot in re.findall(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", f.read())
    ]

pos = [[px, py] for px, py, _, _ in robots]
vel = [(vx, vy) for _, _, vx, vy in robots]


# How to find the tree?
# Find the size of the largest connected component (4-neighborhood)
# If it's larger than 10 - it's probably the tree


def get_size_of_largest_connected_component():
    # Create occupancy grid structure
    grid = [[False for _ in range(wide)] for _ in range(tall)]
    for px, py in pos:
        grid[py][px] = True
    # Find the largest connected component
    unvisited = set([(x, y) for x in range(wide) for y in range(tall) if grid[y][x]])
    visited = set()
    max_len = 0
    while unvisited:
        # Pop the next unvisited
        x_start, y_start = unvisited.pop()
        # Initialize the queue
        queue = [(x_start, y_start)]
        # Check 4-neighborhood
        component = set()
        while queue:
            x0, y0 = queue.pop()
            if (x0, y0) in visited:
                continue
            visited.add((x0, y0))
            component.add((x0, y0))
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                x1, y1 = x0 + dx, y0 + dy
                if x1 < 0 or x1 >= wide or y1 < 0 or y1 >= tall:
                    continue
                if grid[y1][x1]:
                    unvisited.discard((x1, y1))
                    queue.append((x1, y1))
        if len(component) > max_len:
            max_len = len(component)
    return max_len


dim = [wide, tall]
i = 0
while True:
    i += 1
    print(f"Elapsed seconds: {i}", end="\r")
    for k in range(len(robots)):
        for d in range(2):
            pos[k][d] += vel[k][d]
            pos[k][d] %= dim[d]
    n = get_size_of_largest_connected_component()
    if n > 20:
        print(f"\nSTOP - found connected component with size {n}")
        break
