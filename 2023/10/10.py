import math

with open("input.txt", "r") as f:
    pipes = f.read().strip("\n").replace("\n", "")
K = int(math.sqrt(len(pipes)))

# +
# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

# +
# .....
# .F-7.
# .|.|.
# .L-J.
# .....


def index_to_pos(i):
    row = i // K
    col = i % K
    return row, col


def pos_to_index(row, col):
    return row * K + col


N = {"|", "F", "7"}
S = {"|", "L", "J"}
W = {"-", "F", "L"}
E = {"-", "7", "J"}
DIRS = {
    "|": "ns",
    "-": "ew",
    "L": "en",
    "J": "nw",
    "7": "sw",
    "F": "es",
}
DIRS_TO_SYMBOL = {dirs: symbol for symbol, dirs in DIRS.items()}
OPPOSITE = {
    "n": "s",
    "s": "n",
    "e": "w",
    "w": "e",
}

idx = pipes.find("S")
r0, c0 = index_to_pos(idx)

_next = []
if r0 > 0:
    _next.append((r0 - 1, c0, "n"))
if r0 < K - 1:
    _next.append((r0 + 1, c0, "s"))
if c0 > 0:
    _next.append((r0, c0 - 1, "w"))
if c0 < K - 1:
    _next.append((r0, c0 + 1, "e"))

start_dirs = ""
for r1, c1, d01 in _next:
    i1 = pos_to_index(r1, c1)
    d10 = OPPOSITE[d01]
    pipe1 = pipes[i1]
    if pipe1 == ".":
        continue
    if d10 in DIRS[pipe1]:
        start_dirs += d01

start_dirs = "".join(sorted(start_dirs))
start_symbol = DIRS_TO_SYMBOL[start_dirs]
d01 = start_dirs[0]
path = []
path.append(idx)
nsteps = 0
while nsteps < K**2:
    nsteps += 1
    # Go to the next pipe
    if d01 == "n":
        r1 = r0 - 1
        c1 = c0
    elif d01 == "s":
        r1 = r0 + 1
        c1 = c0
    elif d01 == "w":
        r1 = r0
        c1 = c0 - 1
    elif d01 == "e":
        r1 = r0
        c1 = c0 + 1
    else:
        raise RuntimeError(f"Unexpected direction: {d01}")
    i1 = pos_to_index(r1, c1)
    pipe1 = pipes[i1]
    if pipe1 == "S":
        break
    path.append(i1)
    # Get the possible out directions
    # Choose the other one
    r0 = r1
    c0 = c1
    d10 = OPPOSITE[d01]
    d01 = DIRS[pipe1].replace(d10, "")
else:
    raise RuntimeError("LIMIT REACHED")
answer1 = len(path) // 2
print(answer1)  # 6599

path_map = ""
path_map2 = ""
for row in range(K):
    path_row = ""
    path_row2 = ""
    for col in range(K):
        idx = pos_to_index(row, col)
        if idx in path:
            path_row += (
                pipes[idx]
                .replace("S", start_symbol)
                .replace("7", "┐")
                .replace("F", "┌")
                .replace("L", "└")
                .replace("J", "┘")
            )
            path_row2 += "*"
        else:
            path_row += "•"
            path_row2 += "."
    path_map += path_row + "\n"
    path_map2 += path_row2 + "\n"

# with open("path_map<.txt", "w") as f:
#     f.write(path_map)
# with open("path_map2.txt", "w") as f:
#     f.write(path_map2)

path_map1 = path_map.replace("\n", "")
path_map3 = path_map2.replace("\n", "")

x = path_map1[(row * K) : (row * K + col)]
n = x.count("└") + x.count("┘") + x.count("|")
if n % 2 == 0:
    io = "O"
else:
    io = "I"

path_map4 = ""
for row in range(K):
    rrr = ""
    for col in range(K):
        idx = pos_to_index(row, col)
        if path_map1[idx] != "•":
            rrr += path_map1[idx]
        else:
            x = path_map1[(row * K) : (row * K + col)]
            n = x.count("└") + x.count("┘") + x.count("|")
            if n % 2 == 0:
                rrr += "O"
            else:
                rrr += "I"
    path_map4 += rrr + "\n"

# with open("path_map4.txt", "w") as f:
#     f.write(path_map4)

answer_2 = path_map4.count("I")  # CORRECT: 477
print(answer_2)
