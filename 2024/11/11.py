"""
https://adventofcode.com/2024/day/11

Part 1: python 11.py input.txt 25
Part 2: python 11.py input.txt 75
"""

import sys
from collections import defaultdict
from pathlib import Path

from tqdm import tqdm

filename = Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else sys.argv[1]
n_cycles = 25 if len(sys.argv) < 3 else int(sys.argv[2])
verbose = False if len(sys.argv) < 4 else bool(sys.argv[3])


def one_cycle(x: int):
    if x == 0:
        return [1]
    xs = str(x)
    n = len(xs)
    if n % 2 == 0:
        k = n // 2
        return [int(xs[:k]), int(xs[k:])]
    return [x * 2024]


with open(filename) as f:
    elements = {x: 1 for x in map(int, f.read().strip().split(" "))}

# Key idea:
# While the number of all values grows exponentially,
# the number of *unique* values is growing much more slowly.
# It even stabilizes at a constant value after a certain number of cycles.
#
# Instead of applying one_cycle to each value individually (which is very slow),
# we only apply it to unique values, and keep track of counts after each cycle.
#
cycles = range(n_cycles)
if verbose:
    print("Input sequence:", *elements.keys())
else:
    cycles = tqdm(cycles)
for i in cycles:
    if verbose:
        print(i + 1, len(elements), sum(elements.values()))
    counts = list(elements.values())
    mapped = [one_cycle(e) for e in elements]
    elements = defaultdict(int)
    for ee, n in zip(mapped, counts):
        for e in ee:
            elements[e] += n
if verbose:
    print("Final count:")
    print(i + 1, len(elements), sum(elements.values()))
else:
    print(sum(elements.values()))
