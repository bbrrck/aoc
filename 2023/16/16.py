from collections import deque
from enum import Enum

import numpy as np


class Dirs(Enum):
    N = 0
    E = 1
    S = 2
    W = 3


def opposite(d):
    o = (d.value + 2) % 4
    return Dirs(o)


with open("input.txt", "r") as f:
    data = f.read().strip("\n").split("\n")


grid = np.array([[x for x in line] for line in data])
nrows, ncols = grid.shape


def prop(x, y, outgoing, depth=0):
    global grid
    incoming = opposite(outgoing)
    if depth > 1_000_000:
        raise RuntimeError(f"Depth {depth} reached")
    east = (x + 1, y, Dirs.E)
    west = (x - 1, y, Dirs.W)
    north = (x, y - 1, Dirs.N)
    south = (x, y + 1, Dirs.S)
    g = grid[y, x]
    if g == ".":
        if incoming == Dirs.W:
            return [east]
        elif incoming == Dirs.E:
            return [west]
        elif incoming == Dirs.N:
            return [south]
        elif incoming == Dirs.S:
            return [north]
        else:
            raise RuntimeError(f"Invalid dir: {incoming}")
    elif g == "|":
        if incoming in [Dirs.W, Dirs.E]:
            return [north, south]
        elif incoming == Dirs.N:
            return [south]
        elif incoming == Dirs.S:
            return [north]
        else:
            raise RuntimeError(f"Invalid dir: {incoming}")
    elif g == "-":
        if incoming in [Dirs.N, Dirs.S]:
            return [west, east]
        elif incoming == Dirs.W:
            return [east]
        elif incoming == Dirs.E:
            return [west]
        else:
            raise RuntimeError(f"Invalid dir: {incoming}")
    elif g == "\\":
        if incoming == Dirs.W:
            return [south]
        elif incoming == Dirs.E:
            return [north]
        elif incoming == Dirs.N:
            return [east]
        elif incoming == Dirs.S:
            return [west]
        else:
            raise RuntimeError(f"Invalid dir: {incoming}")
    elif g == "/":
        if incoming == Dirs.W:
            return [north]
        elif incoming == Dirs.E:
            return [south]
        elif incoming == Dirs.N:
            return [west]
        elif incoming == Dirs.S:
            return [east]
        else:
            raise RuntimeError(f"Invalid dir: {incoming}")
    else:
        raise RuntimeError(f"Invalid grid symbol: {g}")


energized = np.zeros(grid.shape, dtype=bool)
processed = {}
dirs = deque()
dirs.append((0, 0, Dirs.E))
while len(dirs) > 0:
    x, y, outgoing = dirs.popleft()
    if x < 0 or x >= grid.shape[1]:
        continue
    if y < 0 or y >= grid.shape[0]:
        continue
    if (x, y, outgoing) in processed:
        continue
    processed[(x, y, outgoing)] = True
    energized[y, x] = True
    dirs += prop(x, y, outgoing)
answer_1 = energized.sum()
print(answer_1)

answer_2 = 0
for d in [Dirs.E, Dirs.W, Dirs.N, Dirs.S]:
    for i in range(ncols):
        energized = np.zeros(grid.shape, dtype=bool)
        processed = {}
        dirs = deque()
        if d == Dirs.W:
            initial_dir = (0, i, Dirs.W)
        elif d == Dirs.E:
            initial_dir = (ncols - 1, i, Dirs.E)
        elif d == Dirs.S:
            initial_dir = (i, 0, Dirs.S)
        elif d == Dirs.N:
            initial_dir = (i, ncols - 1, Dirs.N)
        dirs.append(initial_dir)
        while len(dirs) > 0:
            x, y, outgoing = dirs.popleft()
            if x < 0 or x >= grid.shape[1]:
                continue
            if y < 0 or y >= grid.shape[0]:
                continue
            if (x, y, outgoing) in processed:
                continue
            processed[(x, y, outgoing)] = True
            energized[y, x] = True
            dirs += prop(x, y, outgoing)
        e = energized.sum()
        if e > answer_2:
            answer_2 = e
print(answer_2)
