# ruff: noqa: F403 F405

import sys

sys.path.insert(0, "../")
from pathlib import Path
from aoc_tools import *
import itertools
from tqdm import tqdm

# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+
numkey_coords_xy = {
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "0": (1, 3),
    "A": (2, 3),
}

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
dirkey_coords_xy = {
    "^": (1, 0),
    "A": (2, 0),
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1),
}


def get_paths_numkeys(source, target):
    x0, y0 = numkey_coords_xy[source]
    x1, y1 = numkey_coords_xy[target]
    dx = x1 - x0
    dy = y1 - y0
    dirs = ""
    if dx > 0:
        # Go right
        dirs += ">" * dx
    elif dx < 0:
        # Go left
        dirs += "<" * abs(dx)
    if dy > 0:
        # Go down
        dirs += "v" * dy
    elif dy < 0:
        # Go up
        dirs += "^" * abs(dy)
    # Construct all possible permutations of dirs
    options = list(set(itertools.permutations(dirs)))
    # Discard options that pass via the point (0,3) [blank space]
    valid_options = []
    for option in options:
        x, y = x0, y0
        for arrow in option:
            dx, dy = arrows4[arrow]
            x += dx
            y += dy
            if x == 0 and y == 3:
                break
        else:
            valid_options.append("".join(option))
    return valid_options


# Convert code to shortest directional input(s)
# There can be multiple solutions
def get_sequences_numkeys(code):
    source = "A"
    paths = []
    for target in code:
        paths.append(get_paths_numkeys(source, target))
        source = target
    return {"A".join(seq) + "A" for seq in itertools.product(*paths)}


def get_paths_dirkeys(source, target):
    x0, y0 = dirkey_coords_xy[source]
    x1, y1 = dirkey_coords_xy[target]
    dx = x1 - x0
    dy = y1 - y0
    dirs = ""
    if dx > 0:
        # Go right
        dirs += ">" * dx
    elif dx < 0:
        # Go left
        dirs += "<" * abs(dx)
    if dy > 0:
        # Go down
        dirs += "v" * dy
    elif dy < 0:
        # Go up
        dirs += "^" * abs(dy)
    # Construct all possible permutations of dirs
    options = list(set(itertools.permutations(dirs)))
    # Discard options that pass via the point (0,0) [blank space]
    valid_options = []
    for option in options:
        x, y = x0, y0
        for arrow in option:
            dx, dy = arrows4[arrow]
            x += dx
            y += dy
            if x == 0 and y == 0:
                break
        else:
            valid_options.append("".join(option))
    return valid_options


def get_sequences_dirkeys(dircode):
    source = "A"
    paths = []
    for target in dircode:
        paths.append(get_paths_dirkeys(source, target))
        source = target
    return sorted({"A".join(seq) + "A" for seq in itertools.product(*paths)})


# PART 1 - brute force, works
name = Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else Path(sys.argv[1])
ans1 = 0
for code in tqdm(name.open().read().strip("\n").split("\n")):
    k = int(1e32 - 1)
    for seq1 in get_sequences_numkeys(code):
        for seq2 in get_sequences_dirkeys(seq1):
            for seq3 in get_sequences_dirkeys(seq2):
                if len(seq3) < k:
                    k = len(seq3)
    ans1 += k * int(code.replace("A", ""))
print(ans1, ans1 == 163920)
