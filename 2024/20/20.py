# ruff: noqa: F403 F405

import sys

sys.path.insert(0, "../")
from pathlib import Path
from aoc_tools import *
import networkx as nx
from tqdm import tqdm

filename = (
    Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else Path(sys.argv[1])
)

with open(filename) as f:
    grid, n_rows, n_cols = grid_parse(f.read())

source = grid_pos(grid, "S")
target = grid_pos(grid, "E")


def get_edges(x0, y0):
    for dx, dy in dirs4:
        x1, y1 = x0 + dx, y0 + dy
        if y1 < 0 or y1 >= n_rows or x1 < 0 or x1 >= n_cols:
            continue
        if grid[y1][x1] == "#":
            continue
        yield x1, y1


# Construct base graph
G = nx.Graph()
for y0 in range(n_rows):
    for x0 in range(n_cols):
        if grid[y0][x0] == "#":
            continue
        p0 = (x0, y0)
        for p1 in get_edges(*p0):
            G.add_edge(p0, p1)
dist0 = nx.shortest_path_length(G, source, target)
path0 = nx.shortest_path(G, source, target)


# Main insight: all track points are on the shortest path
# Since points are ordered, index in 'path' is the distance from beginning
def count_useful_cheats(cheat_length, min_picoseconds_saved):
    n = 0
    for i0 in tqdm(range(len(path0))):
        p0 = path0[i0]
        for i1 in range(i0 + 1, len(path0)):
            p1 = path0[i1]
            dg = manhattan(*p0, *p1)
            if dg > cheat_length:
                continue
            dp = abs(i1 - i0)
            dd = dp - dg
            if dd >= min_picoseconds_saved:
                n += 1
    return n


# Part 1
print(count_useful_cheats(2, 1 if filename.name == "test.txt" else 100))
# Part 2
print(count_useful_cheats(20, 50 if filename.name == "test.txt" else 100))


# Single for loop
n1 = 0
n2 = 0
for i0 in tqdm(range(len(path0))):
    p0 = path0[i0]
    for i1 in range(i0 + 1, len(path0)):
        p1 = path0[i1]
        dg = manhattan(*p0, *p1)
        if dg > 20:
            continue
        dp = abs(i1 - i0)
        dd = dp - dg
        if dd >= 100:
            if dg <= 2:
                n1 += 1
            n2 += 1
print(n1)
print(n2)
