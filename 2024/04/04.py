import sys
from pathlib import Path

filename = Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else sys.argv[1]

with open(filename) as f:
    data = f.read()

rows = data.splitlines()
grid = data.replace("\n", "")
size = len(rows[0])
columns = [data[i :: size + 1] for i in range(size)]
diagonals = []

for k in range(size):
    # top-right triangle
    diagonals.append(grid[k :: size + 1][: size - k])
    # top-left triangle
    diagonals.append(grid[size - 1 - k :: size - 1][: size - k])
    # only include the main diagonals once
    if k == 0:
        continue
    # bottom-left triangle
    diagonals.append(grid[k * size :: size + 1])
    # bottom-right triangle
    diagonals.append(grid[(k + 1) * size - 1 :: size - 1])


def count_xmas(x: str):
    return x.count("XMAS") + x.count("SAMX")


answer_1 = (
    sum(map(count_xmas, rows))
    + sum(map(count_xmas, columns))
    + sum(map(count_xmas, diagonals))
)
print(answer_1)

answer_2 = 0
for col in range(size - 2):
    for row in range(size - 2):
        # [col, row] marks the top-left corner of the X
        # TL-BR diagonal
        diag1 = grid[col + size * row :: size + 1][:3]
        # TR-BL diagonal
        diag2 = grid[col + size * row + 2 :: size - 1][:3]
        if (diag1.count("MAS") + diag1.count("SAM")) and (
            diag2.count("MAS") + diag2.count("SAM")
        ):
            answer_2 += 1
print(answer_2)
