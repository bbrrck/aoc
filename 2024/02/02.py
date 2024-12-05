import sys
from pathlib import Path

filename = Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else sys.argv[1]

with open(filename) as f:
    data = f.read()

reports = [[int(y) for y in x.split(" ")] for x in data.strip("\n").split("\n")]


def is_increasing(x: list):
    current = x[0]
    for y in x[1:]:
        if y < current:
            return False
        current = y
    return True


def is_decreasing(x: list):
    return is_increasing(x[::-1])


def diffs(x: list):
    return [abs(y - z) for y, z in zip(x[:-1], x[1:])]


def is_safe(x: list):
    d = diffs(x)
    return (is_increasing(x) | is_decreasing(x)) & (min(d) > 0) & (max(d) < 4)


def is_safe_dampened(x: list):
    if is_safe(x):
        return True
    for i in range(len(x)):
        new_x = x[:i] + x[i + 1 :]
        if is_safe(new_x):
            return True
    return False


answer_1 = sum([is_safe(report) for report in reports])
print(answer_1)

answer_2 = sum([is_safe_dampened(report) for report in reports])
print(answer_2)
