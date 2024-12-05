import sys

import networkx as nx

sys.setrecursionlimit(30_000)


with open("input.txt") as f:
    data = f.read().strip("\n").split("\n")

FOREST = "#"
PATH = "."
UP = "^"
RIGHT = ">"
DOWN = "v"
LEFT = "<"
SLOPES = [UP, RIGHT, DOWN, LEFT]
PATH_AND_SLOPES = [PATH] + SLOPES

x_start, y_start = 0, 1
x_end, y_end = len(data) - 1, len(data[-1]) - 2


#### Part 1


def find_possible(x, y):
    global data
    if data[x][y] == UP:
        return [(x - 1, y)]
    if data[x][y] == DOWN:
        return [(x + 1, y)]
    if data[x][y] == LEFT:
        return [(x, y - 1)]
    if data[x][y] == RIGHT:
        return [(x, y + 1)]
    possible = []
    if data[x + 1][y] in PATH_AND_SLOPES:
        possible.append((x + 1, y))
    if data[x - 1][y] in PATH_AND_SLOPES:
        possible.append((x - 1, y))
    if data[x][y - 1] in PATH_AND_SLOPES:
        possible.append((x, y - 1))
    if data[x][y + 1] in PATH_AND_SLOPES:
        possible.append((x, y + 1))
    return possible


def solve(x_last, y_last, visited):
    visited.append((x_last, y_last))
    if (x_last, y_last) == (x_end, y_end):
        return [visited]
    possible = find_possible(x_last, y_last)
    output = []
    for x, y in possible:
        if (x, y) in visited:
            continue
        output += solve(x, y, visited.copy())
    return output


paths = solve(x_start, y_start, [])

answer_1 = max([len(path) - 1 for path in paths])
print(answer_1)


#### Part 2

n = len(data)


def get_directions(x, y, visited=None, return_orientation=False):
    global data
    if data[x][y] == "#":
        return None
    dirs = []
    if x > 0:
        if data[x - 1][y] in PATH_AND_SLOPES:
            if return_orientation:
                dirs.append((x - 1, y, "U"))
            else:
                dirs.append((x - 1, y))
    if x < n - 1:
        if data[x + 1][y] in PATH_AND_SLOPES:
            if return_orientation:
                dirs.append((x + 1, y, "D"))
            else:
                dirs.append((x + 1, y))
    if y > 0:
        if data[x][y - 1] in PATH_AND_SLOPES:
            if return_orientation:
                dirs.append((x, y - 1, "L"))
            else:
                dirs.append((x, y - 1))
    if y < n - 1:
        if data[x][y + 1] in PATH_AND_SLOPES:
            if return_orientation:
                dirs.append((x, y + 1, "R"))
            else:
                dirs.append((x, y + 1))
    if visited:
        dirs = [d for d in dirs if d not in visited]
    return dirs


def is_start_or_end(x, y):
    return len(get_directions(x, y)) == 1


def is_junction(x, y):
    return len(get_directions(x, y)) > 2


start_or_end = []
junctions = []
for x in range(n):
    for y in range(n):
        if data[x][y] == "#":
            continue
        if is_junction(x, y):
            junctions.append((x, y))
        if is_start_or_end(x, y):
            start_or_end.append((x, y))
nodes = start_or_end + junctions


def get_adjacent(x0, y0):
    initial_dirs = get_directions(x0, y0, return_orientation=True)
    adjacent_nodes = []
    for x, y, o in initial_dirs:
        visited = [(x0, y0)]
        while True:
            visited.append((x, y))
            dirs = get_directions(x, y, visited)
            x, y = dirs[0]
            if (x, y) in nodes:
                adjacent_nodes.append((x, y, o, len(visited)))
                break
    return adjacent_nodes


g = nx.Graph()
for x, y in nodes:
    adj = get_adjacent(x, y)
    for xi, yi, oi, wi in sorted(adj):
        g.add_edge((x, y), (xi, yi), weight=wi)


def get_path_len(p):
    l = 0
    for i in range(len(p) - 1):
        n0 = p[i]
        n1 = p[i + 1]
        l += g[n0][n1]["weight"]
    return l


node_start = start_or_end[0]
node_end = start_or_end[1]
all_paths_start_to_end = nx.all_simple_paths(g, node_start, node_end)
answer_2 = 0
for path in all_paths_start_to_end:
    l = get_path_len(path)
    if l > answer_2:
        answer_2 = l
print(answer_2)  # CORRECT: 6506
