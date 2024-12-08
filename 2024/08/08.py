import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

filename = Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else sys.argv[1]

with open(filename) as f:
    data = f.read()  # noqa: F841

GRID = data.strip("\n").replace("\n", "")
SIZE = len(data.splitlines())


def idx_to_pos(idx):
    return (idx // SIZE, idx % SIZE)


# Find positions of antennas, group by type
antennas = defaultdict(list)
for idx, cell in enumerate(GRID):
    if cell == ".":
        continue
    antennas[cell].append(idx_to_pos(idx))


def get_antinodes(pos1, pos2, use_harmonics: bool):
    antinodes = []
    # If using harmonics, the other node is also an antinode
    if use_harmonics:
        antinodes.append(pos1)
        antinodes.append(pos2)
    r1, c1 = pos1
    r2, c2 = pos2
    # Define vector from pos1 to pos2
    dr = r2 - r1
    dc = c2 - c1
    # Antinode 1: pos1 - vector
    ar1, ac1 = r1 - dr, c1 - dc
    while ar1 >= 0 and ar1 < SIZE and ac1 >= 0 and ac1 < SIZE:
        antinodes.append((ar1, ac1))
        if not use_harmonics:
            break
        # If using harmonics, continue in this direction
        ar1, ac1 = ar1 - dr, ac1 - dc
    # Antinode 2: pos2 + vector
    ar2, ac2 = r2 + dr, c2 + dc
    while ar2 >= 0 and ar2 < SIZE and ac2 >= 0 and ac2 < SIZE:
        antinodes.append((ar2, ac2))
        if not use_harmonics:
            break
        # If using harmonics, continue in this direction
        ar2, ac2 = ar2 + dr, ac2 + dc
    return antinodes


antinodes = set(), set()
harmonics = tuple([False, True])
for antenna_type, positions in antennas.items():
    for p1, p2 in combinations(positions, 2):
        for _antinodes, _harmonics in zip(antinodes, harmonics):
            _antinodes.update(get_antinodes(p1, p2, use_harmonics=_harmonics))

answer_1 = len(antinodes[0])
answer_2 = len(antinodes[1])
print(answer_1)
print(answer_2)
