# ruff: noqa: F403 F405

import sys

sys.path.insert(0, "../")
from pathlib import Path
from aoc_tools import *

filename = (
    Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else Path(sys.argv[1])
)

with open(filename) as f:
    keys_and_locks = f.read().split("\n\n")

keys = []
locks = []

for item in keys_and_locks:
    # determine if this is a key (first row is .....) or a lock (first row is #####)
    item = item.replace("\n", "")
    if item.startswith("....."):
        key = []
        for col in range(5):
            for height in range(6):
                if item[(height + 1) * 5 + col] == "#":
                    break
            key.append(5 - height)
        keys.append(key)
    else:
        lock = []
        for col in range(5):
            for height in range(6):
                if item[(height + 1) * 5 + col] == ".":
                    break
            lock.append(height)
        locks.append(lock)


ans1 = 0
for key in keys:
    for lock in locks:
        for k, l in zip(key, lock):
            if k + l > 5:
                break
        else:
            ans1 += 1
print(ans1)

# ------------------------------------------------
