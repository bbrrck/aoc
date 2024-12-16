# ruff: noqa: F403 F405

import sys

sys.path.insert(0, "../")
from pathlib import Path

from aoc_tools import *

filename = Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else sys.argv[1]

with open(filename) as f:
    board1, rules = f.read().split("\n\n")
    board2 = (
        board1.replace("#", "##")
        .replace("O", "[]")
        .replace(".", "..")
        .replace("@", "@.")
    )
    board2, _, n_cols = grid_parse(board2)
    rules = rules.replace("\n", "")


def move_sideways(rx: int, ry: int, arrow: str):
    x, y = rx, ry
    dx, dy = arrows4[arrow]
    boxes = set()
    while True:
        # Check the next cell in the direction
        x += dx
        y += dy
        cell = board2[y][x]
        if cell == "#":
            # Robot ran into wall or obstacle
            return rx, ry
        if cell == "[" or cell == "]":
            # Robot ran into a box
            boxes.add((x, y, cell))
        if cell == ".":
            # Empty cell
            break
    # Move the blocks in queue
    for x, y, cell in boxes:
        board2[y + dy][x + dx] = cell
    # Move the robot
    board2[ry][rx] = "."
    rx += dx
    ry += dy
    board2[ry][rx] = "@"
    return rx, ry


def move_updown(rx: int, ry: int, arrow: str):
    x0, x1, y = rx, rx, ry
    dx, dy = arrows4[arrow]
    boxes = set()
    while True:
        y += dy
        is_blocked = False
        xs = range(x0, x1 + 1)
        x0, x1 = n_cols, 0  # init next range
        for x in xs:
            cell = board2[y][x]
            if cell == "#":
                # Robot cannot move
                return rx, ry
            elif cell == "[":
                # There is a box
                is_blocked = True
                x0, x1 = min(x0, x), max(x1, x + 1)
                boxes.add((x, y, board2[y][x]))
                boxes.add((x + 1, y, board2[y][x + 1]))
            elif cell == "]":
                # There is a box
                is_blocked = True
                x0, x1 = min(x0, x - 1), max(x1, x)
                boxes.add((x, y, board2[y][x]))
                boxes.add((x - 1, y, board2[y][x + -1]))
        if is_blocked:
            # Robot might be able to move, but there are boxes in the way
            # We need to continue checking
            continue
        break
    # If we have reached here --> robot and boxes can move
    # Push the boxes
    # -- first pass: clear the boxes
    for x, y, c in boxes:
        board2[y][x] = "."
    # -- second pass: add the boxes
    for x, y, c in boxes:
        board2[y + dy][x] = c
    # Move the robot
    board2[ry][rx] = "."
    rx += dx
    ry += dy
    board2[ry][rx] = "@"
    return rx, ry


# Find robot's starting position
rx, ry = grid_pos(board2, "@")

# Move the robot based on the rules
move = {
    "<": move_sideways,
    ">": move_sideways,
    "^": move_updown,
    "v": move_updown,
}
for counter, arrow in enumerate(rules):
    rx, ry = move[arrow](rx, ry, arrow)

# Output: sum of all boxes' GPS coordinates
print(
    answer_2 := sum([100 * y + x for x, y in grid_all(board2, "[")]),
    answer_2 == 1386070,
    sep="\n",
)
