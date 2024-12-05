import sys
from pathlib import Path

filename = Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else sys.argv[1]

with open(filename) as f:
    data = [line.split("   ") for line in f.read().strip("\n").split("\n")]

list0 = [int(x[0]) for x in data]
list1 = [int(x[1]) for x in data]
slist0 = sorted(list0)
slist1 = sorted(list1)
diffs = [abs(x - y) for x, y in zip(slist0, slist1)]

answer_1 = sum(diffs)
print(answer_1)

answer_2 = sum([x * list1.count(x) for x in list0])
print(answer_2)
