import sys
from pathlib import Path

filename = Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else sys.argv[1]

with open(filename) as f:
    data = f.read()  # noqa: F841

board, rules = data.split("\n\n")
board = [list(row) for row in board.split("\n")]
size = len(board)
rules = rules.replace("\n", "")
dir = {
    "<": (-1, 0),
    ">": (1, 0),
    "v": (0, 1),
    "^": (0, -1),
}

LINE_UP = "\033[1A"
LINE_CLEAR = "\x1b[2K"

first = True
counter = 0


def show():
    return  # disable
    global first
    global counter
    _board = "." * counter + "\n"
    _board += "\n".join(["".join(row) for row in board])
    if not first:
        _board = (LINE_UP + LINE_CLEAR) * (size + 2) + _board
    print(_board)
    _ = input()
    first = False
    counter += 1


# robot starting position
rx, ry = [(x, y) for y, r in enumerate(board) for x, c in enumerate(r) if c == "@"][0]

show()
for rule in rules:
    dx, dy = dir[rule]
    x, y = rx, ry
    can_move = True
    queue = []
    while True:
        # Check the next cell in the direction
        x += dx
        y += dy
        c = board[y][x]
        # If the next cell is a wall or obstacle, stop - we cannot move anything
        if c == "#":
            can_move = False
            break
        # If the next cell is a box, it could be moved - add it to the move queue and continue walking in the direction
        if c == "O":
            queue.append((x, y))
        # If the next cell is empty, move all boxes in the queue, as well as the robot
        if c == ".":
            break
    if can_move:
        # Move the blocks
        for x, y in queue:
            board[y + dy][x + dx] = "O"
        # Move the robot
        board[ry][rx] = "."
        rx += dx
        ry += dy
        board[ry][rx] = "@"
    show()


answer_1 = 0
for y, row in enumerate(board):
    for x, c in enumerate(row):
        if c == "O":
            answer_1 += 100 * y + x
print(answer_1)
