import re
from copy import deepcopy

import numpy as np

with open("input.txt") as f:
    data = f.read().strip("\n").split("\n")
    blocks_raw = [
        [
            int(x)
            for x in re.match(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)", line).groups()
        ]
        for line in data
    ]

V = np.array(blocks_raw)
V0 = V[:, :3]
V1 = V[:, 3:]

min_x, min_y, min_z = np.concatenate([V0, V1]).min(axis=0)
max_x, max_y, max_z = np.concatenate([V0, V1]).max(axis=0)


class Block:
    def __init__(self, idx, *params) -> None:
        self.idx = idx
        self.x0, self.y0, self.z0, self.x1, self.y1, self.z1 = params
        # mark the next block, not the end block
        self.x1 += 1
        self.y1 += 1
        self.z1 += 1
        # length in each direction
        self.dx = self.x1 - self.x0
        self.dy = self.y1 - self.y0
        self.dz = self.z1 - self.z0
        # block orientation
        self.orientation = "x" if self.dx > 1 else ("y" if self.dy > 1 else "z")
        self.store_bottom_bricks()

    def can_fall(self):
        global B
        if self.z0 == 1:
            return False
        for x, y, z in self.bottom_bricks:
            if B[z - 1, y, x] != 0:
                return False
        return True

    def mark(self):
        global B
        for x in range(self.x0, self.x1):
            for y in range(self.y0, self.y1):
                for z in range(self.z0, self.z1):
                    B[z, y, x] = self.idx

    def unmark(self):
        global B
        for x in range(self.x0, self.x1):
            for y in range(self.y0, self.y1):
                for z in range(self.z0, self.z1):
                    B[z, y, x] = 0

    def move_down(self, verbose=True):
        # if verbose:
        #     print(f"Block {self.idx} falls from level {self.z0} to {self.z0-1}")
        self.unmark()
        self.z0 -= 1
        self.z1 -= 1
        self.mark()
        self.store_bottom_bricks()

    def store_bottom_bricks(self):
        # get a list of bottom bricks
        self.bottom_bricks = []
        for x in range(self.x0, self.x1):
            for y in range(self.y0, self.y1):
                self.bottom_bricks.append((x, y, self.z0))

    def __str__(self):
        return f"{self.idx} {self.orientation} : {self.x0},{self.y0},{self.z0}~{self.x1-1},{self.y1-1},{self.z1-1} [{self.dx},{self.dy},{self.dz}]"

    def __repr__(self):
        return self.__str__()

    def __gt__(self, block):
        return self.z0 > block.z0


# Grid occupancy
B = np.zeros([max_z + 1, max_y + 1, max_x + 1], dtype=np.int32)

blocks = []

for idx, params in enumerate(blocks_raw):
    block = Block(idx + 1, *params)
    block.mark()
    blocks.append(block)

for block in sorted(blocks):
    # print(block)
    while block.can_fall():
        block.move_down(verbose=True)


with open("test.txt", "w") as f:
    for z in reversed(range(min_z, max_z)):
        b = B[z, :, :]
        if b.sum() == 0:
            continue
        f.write(f"\nLevel {z}:\n")
        np.savetxt(f, b, fmt="%5d")

answer_1 = 0
for block in blocks:
    # print(block.idx)
    block.unmark()
    for other in blocks:
        if other == block:
            continue
        if other.can_fall():
            # print(f"    {other.idx} is supported")
            break
    else:
        # print("    does not support any blocks")
        answer_1 += 1
    block.mark()
print(answer_1)

# Grid occupancy
B = np.zeros([max_z + 1, max_y + 1, max_x + 1], dtype=np.int32)
blocks = []

for idx, params in enumerate(blocks_raw):
    block = Block(idx + 1, *params)
    block.mark()
    blocks.append(block)

blocks = sorted(blocks)

for block in blocks:
    while block.can_fall():
        block.move_down(verbose=True)

# Take a snapshot of the current state
initial_blocks = deepcopy(blocks)
initial_B = deepcopy(B)

answer_2_n_falls = 0
for current_block in initial_blocks:
    # print(current_block.idx)

    # Restore the initial state
    B = deepcopy(initial_B)
    blocks = deepcopy(initial_blocks)

    # Unmark the current block in B
    current_block.unmark()

    # Loop over other blocks
    for other_block in sorted(blocks):
        if other_block.idx == current_block.idx:
            continue
        if other_block.can_fall():
            answer_2_n_falls += 1
            # print(f"    block {other_block.idx} falls")
            while other_block.can_fall():
                other_block.move_down(verbose=False)
print(answer_2_n_falls)
