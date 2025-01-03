# ruff: noqa: F403 F405

import sys

sys.path.insert(0, "../")
from pathlib import Path
from aoc_tools import *

filename = (
    Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else Path(sys.argv[1])
)

with open(filename) as f:
    val, ops_raw = f.read().split("\n\n")

val = {row.split(": ")[0]: row.split(": ")[1] == "1" for row in val.split("\n")}
ops = []
out = []
for x in ops_raw.split("\n"):
    i, o = x.split(" -> ")
    i0, op, i1 = i.split(" ")
    ops.append((i0, op, i1, o))
    if o.startswith("z"):
        out.append(o)

# Apply ops in the order such that the input of each op is available
niter = 0
while True:
    # Check if output values are available
    for o in out:
        if o not in val:
            break
    else:
        break
    # Apply ops
    niter += 1
    # print(niter)
    for i0, op, i1, o in ops:
        if i0 not in val:
            continue
        if i1 not in val:
            continue
        if op == "XOR":
            val[o] = val[i0] ^ val[i1]
        elif op == "OR":
            val[o] = val[i0] | val[i1]
        elif op == "AND":
            val[o] = val[i0] & val[i1]
        else:
            raise ValueError("Invalid op")

ans1 = 0
for o in out:
    pow = int(o[1:])
    ans1 += val[o] * 2**pow


# print(ans1)  # 45213383376616 IS CORRECT

# PART 2
# Need to find ops which sum the two input numbers
# Get the two input numbers
x = 0
y = 0
for k, v in val.items():
    if k.startswith("x"):
        pow = int(k[1:])
        x += v * 2**pow
    elif k.startswith("y"):
        pow = int(k[1:])
        y += v * 2**pow
    else:
        continue

if filename.name == "test2.txt":
    exp = x & y
else:
    exp = x + y  # This is the expected sum that the system is supposed to produce
print(f"{exp  = }")
print(f"{ans1 = }")
