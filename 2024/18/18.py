# ruff: noqa: F403 F405

import sys

sys.path.insert(0, "../")
from pathlib import Path
from aoc_tools import *
import networkx as nx

filename = (
    Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else Path(sys.argv[1])
)

with open(filename) as f:
    all_blocks = [
        tuple(map(int, line.split(","))) for line in f.read().strip("\n").split("\n")
    ]


if filename.name == "test.txt":
    size = 7
    n_blocks_part_1 = 12
else:
    size = 71
    n_blocks_part_1 = 1024


def shortest_path_length(n_blocks):
    blocks = all_blocks[:n_blocks]
    graph = nx.Graph()
    for r0 in range(size):
        for c0 in range(size):
            if (r0, c0) in blocks:
                continue
            for dr, dc in dirs4:
                r1, c1 = r0 + dr, c0 + dc
                if r1 < 0 or r1 >= size or c1 < 0 or c1 >= size or (r1, c1) in blocks:
                    continue
                graph.add_edge((r0, c0), (r1, c1))
    source = (0, 0)
    target = (size - 1, size - 1)
    try:
        return nx.shortest_path_length(graph, source, target)
    except:  # noqa: E722
        return None


# Part 1
print(shortest_path_length(n_blocks_part_1))

# Part 2 - brute force
for n_blocks in range(n_blocks_part_1, len(all_blocks)):
    if shortest_path_length(n_blocks) is None:
        print(n_blocks + 1, all_blocks[n_blocks - 1])
        break
