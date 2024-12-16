# ruff: noqa: F403 F405

import sys

sys.path.insert(0, "../")
from pathlib import Path
from aoc_tools import *

filename = Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else sys.argv[1]

with open(filename) as f:
    board, rules = f.read().split("\n\n")
    board, n_rows, n_cols = grid_parse(board)
    rules = rules.replace("\n", "")

# Find robot's starting position
rx, ry = grid_pos(board, "@")

for rule in rules:
    dx, dy = arrows4[rule]
    x, y = rx, ry
    boxes = []
    can_move = True
    while True:
        # Check the next cell in the direction
        x += dx
        y += dy
        cell = board[y][x]
        # Stop if the next cell is wall or obstacle -> robot cannot move
        if cell == "#":
            can_move = False
            break
        # If the next cell is a box, robot might be able to move
        # Add the box to queue and continue walking in the same direction
        if cell == "O":
            boxes.append((x, y))
        # If the next cell is empty, robot and boxes can move
        if cell == ".":
            break
    # If the robot cannot move, continue to the next rule
    if not can_move:
        continue
    # Otherwise, move the blocks ...
    for x, y in boxes:
        board[y + dy][x + dx] = "O"
    # ... and move the robot.
    board[ry][rx] = "."
    rx += dx
    ry += dy
    board[ry][rx] = "@"

# Compute sum of all boxes' GPS coordinates
print(sum([100 * y + x for x, y in grid_all(board, "O")]))
