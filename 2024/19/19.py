import sys
from functools import lru_cache
from pathlib import Path

filename = (
    Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else Path(sys.argv[1])
)

with open(filename) as f:
    data = f.read()

towels, designs = data.split("\n\n")
towels = towels.split(", ")
designs = designs.split("\n")


@lru_cache
def test(x):
    if x == "":
        return 1
    n = 0
    for t in towels:
        if x.startswith(t):
            n += test(x[len(t) :])
    return n


answer_1 = 0
answer_2 = 0
for design in designs:
    n = test(design)
    answer_1 += int(n > 0)
    answer_2 += n
print(answer_1)
print(answer_2)
