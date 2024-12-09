import sys
from collections import deque
from pathlib import Path

from tqdm import tqdm

filename = Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else sys.argv[1]

with open(filename) as f:
    data = list(map(int, f.read().strip("\n")))  # noqa: F841


def seq_to_str(seq):
    return "".join([str(x) if x >= 0 else "." for x in seq])


# Split input into blocks and spaces
blocks = [(index, "B", size) for index, size in enumerate(data[::2])]
spaces = [(index, "S", size) for index, size in enumerate(data[1::2])]

# ------------------------------------------------
# Part 1
# ------------------------------------------------
unordered = deque(sorted(blocks + spaces))
ordered = []
while unordered:
    idx, type, size = unordered.popleft()
    # If Block: Add it to the end of the sequence
    if type == "B":
        seq = [idx] * size
        ordered += seq
        continue
    # If Space: Move end blocks into the space
    while size > 0:
        # If there are no blocks left, exit
        if not unordered:
            break
        # Get the end block
        eidx, etype, esize = unordered.pop()
        if etype == "S":
            continue
        if esize <= size:
            # End block fits into the remaining space --> add it to that space
            seq = [eidx] * esize
            ordered += seq
            size -= esize
        else:
            # End block does not fit --> split it in two parts
            # -- first part: move it to the free space
            seq = [eidx] * size
            ordered += seq
            esize -= size
            size = 0
            # -- second part: keep it at the end of the sequence
            unordered.append((eidx, etype, esize - size))
            # the original space is now occupied --> stop
            break
answer_1 = sum([x * y for x, y in enumerate(ordered)])
print(answer_1)

# ------------------------------------------------
# Part 2
# ------------------------------------------------
elements = list(sorted(blocks + spaces))
for block in tqdm(list(reversed(blocks))):
    bpos = elements.index(block)
    bidx, btype, bsize = block
    # Iterate over spaces BEFORE the block
    for k, space in enumerate(elements[:bpos]):
        sidx, stype, ssize = space
        # Skip other blocks
        if stype == "B" or stype == "X":
            continue
        if bsize > ssize:
            # Block does not fit into the space
            continue
        # delete the original block
        elements[bpos] = (bidx, "S", bsize)
        # Block fits into space, put it there and make it static
        if ssize == bsize:
            # if the block fits exactly, turn the space into a block
            elements[k] = (bidx, "X", bsize)
        else:
            # otherwise, split the space
            elements[k] = (sidx, "S", ssize - bsize)
            elements.insert(k, (bidx, "X", bsize))
        break
    else:
        # Block does not fit into any of the spaces --> make it static
        elements[bpos] = (bidx, "X", bsize)
pos = 0
answer_2 = 0
for i, t, n in elements:
    if t == "S":
        pos += n
    else:
        for k in range(n):
            answer_2 += i * pos
            pos += 1
print(answer_2)


# ------------------------------------------------
# Example:
# 2333133121414131402
#
# ------------------------------------------------
# Part 1:
#
# 00...111...2...333.44.5555.6666.777.888899
# 009..111...2...333.44.5555.6666.777.88889.
# 0099.111...2...333.44.5555.6666.777.8888..
# 00998111...2...333.44.5555.6666.777.888...
# 009981118..2...333.44.5555.6666.777.88....
# 0099811188.2...333.44.5555.6666.777.8.....
# 009981118882...333.44.5555.6666.777.......
# 0099811188827..333.44.5555.6666.77........
# 00998111888277.333.44.5555.6666.7.........
# 009981118882777333.44.5555.6666...........
# 009981118882777333644.5555.666............
# 00998111888277733364465555.66.............
# 0099811188827773336446555566..............
#
# ------------------------------------------------
# Part 2:
#
# 00...111...2...333.44.5555.6666.777.888899
# 0099.111...2...333.44.5555.6666.777.8888..
# 0099.1117772...333.44.5555.6666.....8888..
# 0099.111777244.333....5555.6666.....8888..
# 00992111777.44.333....5555.6666.....8888..
# ------------------------------------------------
