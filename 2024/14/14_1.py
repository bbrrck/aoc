import re
import sys
from pathlib import Path

filename = (
    Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else Path(sys.argv[1])
)

# Define grid dimensions
if filename.name == "test.txt":
    dim = (11, 7)
elif filename.name == "input.txt":
    dim = (101, 103)
else:
    raise RuntimeError(f"Unknown input file: {filename}")

# Get initial robot positions and their velocities
with open(filename) as f:
    robots = [
        list(map(int, robot))
        for robot in re.findall(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", f.read())
    ]
pos = [[px, py] for px, py, _, _ in robots]
vel = [(vx, vy) for _, _, vx, vy in robots]

# Simulate robot movement for 100 seconds
n_robots = len(robots)
n_seconds = 100
for i in range(n_seconds):
    for k in range(n_robots):
        for d in range(2):
            pos[k][d] += vel[k][d]
            pos[k][d] %= dim[d]

# Count number of robots in every quadrant
mx, my = dim[0] // 2, dim[1] // 2
N = [0, 0, 0, 0]
for px, py in pos:
    if px < mx:
        if py < my:
            N[0] += 1
        elif py > my:
            N[1] += 1
    elif px > mx:
        if py < my:
            N[2] += 1
        if py > my:
            N[3] += 1

# Compute final safety factor
score = 1
for n in N:
    score *= n
print(score)
