# ruff: noqa: F403 F405

import sys

sys.path.insert(0, "../")
from pathlib import Path
from aoc_tools import *
import networkx as nx
from collections import defaultdict

filename = (
    Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else Path(sys.argv[1])
)

with open(filename) as f:
    grid, n_rows, n_cols = grid_parse(f.read())

source = grid_pos(grid, "S")
target = grid_pos(grid, "E")
G = nx.Graph()

print(f"{source = }")
print(f"{target = }")


def l():
    return nx.shortest_path_length(G, source, target)


def get_edges(x, y):
    for dx, dy in dirs4:
        x1, y1 = x + dx, y + dy
        if y1 < 0 or y1 >= n_rows or x1 < 0 or x1 >= n_cols:
            continue
        if grid[y1][x1] == "#":
            continue
        yield x1, y1


# Construct base graph
G0 = nx.DiGraph()
for y0 in range(n_rows):
    for x0 in range(n_cols):
        if grid[y0][x0] == "#":
            continue
        p0 = (x0, y0)
        for p1 in get_edges(*p0):
            G0.add_edge(p0, p1)
            G0.add_edge(p1, p0)
G = G0.copy()
l0 = l()

# Remove each wall and see if path length changes
diff_counts = defaultdict(int)
n = 0
for y0 in range(n_rows):
    for x0 in range(n_cols):
        print(y0, x0)
        if grid[y0][x0] != "#":
            continue
        G = G0.copy()
        p0 = (x0, y0)
        for p1 in get_edges(*p0):
            G.add_edge(p0, p1)
            G.add_edge(p1, p0)
        diff = l0 - l()
        if diff >= 100:
            n += 1
print(n)
