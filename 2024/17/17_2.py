import itertools
import re
import sys
from pathlib import Path

from common import run_program

filename = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("input.txt")
_, b, c, *prog = map(int, re.findall(r"(\d+)", filename.open().read()))

# Solution is somewhere between these two numbers
# 8**15 =  35184372088832 = 0o1000000000000000
# 8**16 = 281474976710656 = 0o10000000000000000

# Initialize the list of possible bits to
# -- [  1,2,...,7] for bit  15 (index 0)
# -- [0,1,2,...,7] for bits 14 to 0 (indices 1 to 15)
possible_bits = [list(range(1 if i == 0 else 0, 8)) for i in range(16)]

# Reduce the search space
# k - index of the last bit to check
for k in range(16):
    print(f"... checking first {k + 1:2d} bit{'s' if k > 0 else ' '} of 16 ...")
    # Check all possible combinations of the first k+1 bits
    input_combinations = itertools.product(*possible_bits[: k + 1])
    valid_combinations = []
    for bits in input_combinations:
        a = 0
        # Construct initial value of register A from bits
        # idx = 15 - bit_position
        for idx, bit in enumerate(bits):
            a += bit * 8 ** (15 - idx)
        # Run the program for this value of A
        out = run_program(a, b, c, prog)
        # Check if the last k+1 bits of the output match the last k+1 bits of the program
        if prog[-k - 1 :] != out[-k - 1 :]:
            continue
        # If yes, this is a valid combination so far
        valid_combinations.append(bits)
    # Update lists of possible bits - they now contain fewer options
    for kk in range(k + 1):
        possible_bits[kk] = sorted(list(set([x[kk] for x in valid_combinations])))

possible_combinations = list(itertools.product(*possible_bits))
print(f"Done, reduced search space to {len(possible_combinations)} combinations.")

print("Searching for combinations that reproduce the program...")
regA_options = []
for bits in possible_combinations:
    a = 0
    for idx, bit in enumerate(bits):
        a += bit * 8 ** (15 - idx)
    out = run_program(a, b, c, prog)
    if out == prog:
        regA_options.append(a)

print(f"Found {len(regA_options)} values of register A that reproduce the program:")
print(*regA_options, sep="\n")
print("Smallest value from the above list (part 2 answer):")
print(min(regA_options))
