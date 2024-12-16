import sys
from pathlib import Path
import os
import time
from rich import Console

console = Console()


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


filename = Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else sys.argv[1]

with open(filename) as f:
    data = f.read()  # noqa: F841

board, rules = data.split("\n\n")

# Large board
# If the tile is #, the new map contains ## instead.
# If the tile is O, the new map contains [] instead.
# If the tile is ., the new map contains .. instead.
# If the tile is @, the new map contains @. instead.
board = (
    board.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
)
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

K = os.get_terminal_size().columns


def show(counter):
    global first
    _board = ""
    _board += "\n".join(["".join(row) for row in board]) + "\n"
    _board = _board.replace("@", f"{bcolors.OKGREEN}@" + bcolors.ENDC)
    _board += "next: " + (rules[counter] if counter < len(rules) else "END") + "\n"
    _board += f"done: {counter} of {len(rules)}\n"
    # for i in range(len(rules) // K):
    #     i0 = i * K
    #     i1 = (i + 1) * K
    #     if counter < i0:
    #         _board += "\n" + rules[i0:i1]
    #     elif counter >= i1:
    #         _board += "\n" + bcolors.OKGREEN + rules[i0:i1]
    #     else:
    #         # counter is in range [i0, i1)
    #         _board += (
    #             "\n"
    #             + bcolors.OKGREEN
    #             + rules[i0:counter]
    #             + bcolors.OKCYAN
    #             + rules[counter]
    #             + bcolors.ENDC
    #             + rules[counter + 1 : i1]
    #         )
    rev = (LINE_UP + LINE_CLEAR) * (_board.count("\n") + 2)
    print((rev if not first else "") + _board)
    # _ = input()
    time.sleep(0.01)
    first = False


show(0)


# robot starting position
rx, ry = [(x, y) for y, r in enumerate(board) for x, c in enumerate(r) if c == "@"][0]
for counter, rule in enumerate(rules):
    if rule in ("<", ">"):
        x, y = rx, ry
        dx, dy = dir[rule]
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
            if c == "[" or c == "]":
                queue.append((x, y, c))
            # If the next cell is empty, move all boxes in the queue, as well as the robot
            if c == ".":
                break
        if can_move:
            # Move the blocks
            for x, y, c in queue:
                board[y + dy][x + dx] = c
            # Move the robot
            board[ry][rx] = "."
            rx += dx
            ry += dy
            board[ry][rx] = "@"
    else:
        # handle top and down
        x_min, x_max, y = rx, rx, ry
        dx, dy = dir[rule]
        can_move = True
        queue = set()
        while True:
            # Check the next cells in the direction
            y += dy
            is_blocked = False
            # print(f"{y = }")
            trim = set()
            new_x_min = 100000
            new_x_max = -100000
            for xx in range(x_min, x_max + 1):
                cx = board[y][xx]
                # print(y, xx, cx)
                if cx == "#":
                    # print("BLOCKED by #")
                    can_move = False
                    is_blocked = True
                    break
                elif cx == "[":
                    # print("BLOCKED by [")
                    new_x_min = min(new_x_min, xx)
                    new_x_max = max(new_x_max, xx + 1)
                    queue.add((xx, y, board[y][xx]))
                    queue.add((xx + 1, y, board[y][xx + 1]))
                    is_blocked = True
                elif cx == "]":
                    # print("BLOCKED by ]")
                    new_x_min = min(new_x_min, xx - 1)
                    new_x_max = max(new_x_max, xx)
                    queue.add((xx, y, board[y][xx]))
                    queue.add((xx - 1, y, board[y][xx + -1]))
                    is_blocked = True
                # elif cx == ".":
                #     # this
                #     trim.add(xx)
            x_min = new_x_min
            x_max = new_x_max
            # We cannot move anything
            if not can_move:
                break
            # We can move, and we are blocked
            if is_blocked:
                continue
            break
        if can_move:
            # Push the boxes
            for x, y, c in queue:
                board[y][x] = "."
            for x, y, c in queue:
                board[y + dy][x] = c
            # Move the robot
            board[ry][rx] = "."
            rx += dx
            ry += dy
            board[ry][rx] = "@"
    show(counter + 1)

answer_2 = 0
for y, row in enumerate(board):
    for x, c in enumerate(row):
        if c == "[":
            answer_2 += 100 * y + x
print(answer_2)
