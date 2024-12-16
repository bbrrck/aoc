import sys
from pathlib import Path
import networkx as nx

filename = Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else sys.argv[1]

with open(filename) as f:
    data = f.read()  # noqa: F841

maze = [list(row) for row in data.split("\n")]
n_rows = len(maze)
n_cols = len(maze[0])

# ---------------------------------------------------------------------------------------
# Approach: use Djikstra on the following graph:
# -- nodes (i, j, d) where `d` is the direction the Reindeer is facing.
# -- directed edges ((i0,j0,d0), (i1,j1,d1), w) where w is the cost
#    of going from (i0,j0,d0) to (i1,j1,d1):
#    -- w = 1    if d0 == "^" == d1 and (i1,j1) == (i0-1,j0)
#    -- w = 1    if d0 == ">" == d1 and (i1,j1) == (i0,j0+1)
#    -- w = 1    if d0 == "v" == d1 and (i1,j1) == (i0+1,j0)
#    -- w = 1    if d0 == "<" == d1 and (i1,j1) == (i0,j0-1)
#    -- w = 1000 if angle(d0,d1) == 90 degrees and (i1,j1) == (i0,j0)
# --------------------------------------------------------------------------------------

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

DIR_TO_VECTOR = {
    NORTH: (-1, 0),
    EAST: (0, 1),
    SOUTH: (1, 0),
    WEST: (0, -1),
}

# Construct the graph
G = nx.DiGraph()
source = None
target = None
for i0, row in enumerate(maze):
    for j0, c0 in enumerate(row):
        # If cell is a wall, skip it
        if c0 == "#":
            continue
        if c0 == "S":
            # Reindeer start position
            source = (i0, j0, EAST)
        if c0 == "E":
            # Reindeer end position
            target = (i0, j0)
        # Add 'turning' edges
        for dir in range(4):
            n0 = (i0, j0, dir)
            n1 = (i0, j0, (dir + 1) % 4)
            G.add_edge(n0, n1, weight=1000)
            G.add_edge(n1, n0, weight=1000)
        # Add 'moving' edges
        for dir, (di, dj) in DIR_TO_VECTOR.items():
            i1, j1 = i0 + di, j0 + dj
            if i1 < 0 or i1 >= n_rows or j1 < 0 or j1 >= n_cols:
                continue  # We ran into outside wall
            c1 = maze[i1][j1]
            if c1 == "#":
                continue  # We ran into inside wall
            # Add edge representing a move from current tile
            # to the neighboring tile in the given direction
            n0 = (i0, j0, dir)
            n1 = (i1, j1, dir)
            G.add_edge(n0, n1, weight=1)

# ------------------------------------------------
# Part 1
# ------------------------------------------------
shortest_distance = min(
    [
        nx.shortest_path_length(G, source, (*target, dir), weight="weight")
        for dir in DIR_TO_VECTOR
    ]
)
print(shortest_distance)

# ------------------------------------------------
# Part 2
# ------------------------------------------------
best_tiles = set()
for dir in DIR_TO_VECTOR:
    length = nx.shortest_path_length(G, source, (*target, dir), weight="weight")
    if length > shortest_distance:
        continue
    for path in nx.all_shortest_paths(G, source, (*target, dir), weight="weight"):
        for i, j, _ in path:
            best_tiles.add((i, j))
n_best_tiles = len(best_tiles)
print(n_best_tiles)

# ------------------------------------------------
