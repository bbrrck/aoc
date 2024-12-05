import re
import sys
from pathlib import Path

filename = Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else sys.argv[1]

with open(filename) as f:
    data = f.read()

# ------------------------------------------------

answer_1 = sum([int(x) * int(y) for x, y in re.findall(r"mul\((\d+),(\d+)\)", data)])
print(answer_1)

# ------------------------------------------------

answer_2 = 0
enable = True
for x, y, do, dont in re.findall(r"mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))", data):
    if do != "":
        enable = True
    elif dont != "":
        enable = False
    else:
        answer_2 += int(x) * int(y) if enable else 0
print(answer_2)

# ------------------------------------------------
