import re
import sys
from pathlib import Path

filename = (
    Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else Path(sys.argv[1])
)

if filename.name == "test.txt":
    wide = 11
    tall = 7
elif filename.name == "input.txt":
    wide = 101
    tall = 103
else:
    raise RuntimeError(f"Unknown input file: {filename}")

with open(filename) as f:
    robots = [
        list(map(int, robot))
        for robot in re.findall(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", f.read())
    ]

# Display robots in terminal
LINE_UP = "\033[1A"
LINE_CLEAR = "\x1b[2K"
niter = 0
go_back = False
n_steps_no_prompt = 0
while True:
    if go_back:
        niter -= 1
    else:
        niter += 1
    for k, (px, py, vx, vy) in enumerate(robots):
        if go_back:
            robots[k] = [(px - vx) % wide, (py - vy) % tall, vx, vy]
        else:
            robots[k] = [(px + vx) % wide, (py + vy) % tall, vx, vy]
    if n_steps_no_prompt > 0:
        n_steps_no_prompt -= 1
        continue
    grid = [["." for _ in range(wide)] for _ in range(tall)]
    for px, py, _, _ in robots:
        grid[py][px] = "#"
    print(
        (LINE_UP + LINE_CLEAR) * (tall + 2)
        + "\n".join(["".join(line) for line in grid])
        + f"\n{niter}"
    )
    x = input()
    if x == "":
        continue
    elif x == "b":
        go_back = True
    elif x == "f":
        go_back = False
    elif x[0] == "s":
        n_steps_no_prompt = int(x[1:])
