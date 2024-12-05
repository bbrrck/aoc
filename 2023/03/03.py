import numpy as np

with open("input.txt", "r") as f:
    lines = f.read().strip("\n").split("\n")

MAX_LEN = 140
DIGITS = [str(i) for i in range(10)]
DIGITS_AND_DOT = DIGITS.copy() + ["."]


def find_numbers(line):
    """Find all numbers in a line.

    A number is defined by a tuple (position, length).
    """
    numbers = []
    position = -1
    length = 0
    for idx, char in enumerate(line):
        # Character is a digit
        if char in DIGITS:
            # Starting a new number
            if position == -1:
                position = idx
            # Increase the length of the current number
            length += 1
            # If this is the last
        # Character is a symbol or a dot, or we are at the end
        else:
            if position > -1:
                # Previous character was a digit, save the number
                numbers.append((position, length))
            # Reset the position and length
            position = -1
            length = 0
        # Edge case: end of line
        if idx == MAX_LEN - 1 and position > -1:
            numbers.append((position, length))
    return numbers


def is_symbol(line, idx, verbose=False):
    if idx < 0 or idx > MAX_LEN - 1:
        if verbose:
            print(f"{idx = }, is_symbol = False")
        return False
    is_symbol = line[idx] not in DIGITS_AND_DOT
    if verbose:
        print(f"{idx = }, char = {line[idx]}, {is_symbol = }")
    return is_symbol


def is_part_number(number, line, previous_line, next_line):
    """Check if number is a part number.

    A number is a part number if it is adjacent to a symbol, even diagonally.
    """
    position, length = number
    # Check previous and next char in current line
    if is_symbol(line, position - 1):
        return True
    if is_symbol(line, position + length):
        return True
    # Check previous line
    if previous_line is not None:
        for idx in range(position - 1, position + length + 1):
            if is_symbol(previous_line, idx):
                return True
    # Check next line
    if next_line is not None:
        for idx in range(position - 1, position + length + 1):
            if is_symbol(next_line, idx):
                return True
    return False


answer_1 = 0
for line_no, line in enumerate(lines):
    numbers = find_numbers(line)
    previous_line = None
    if line_no > 0:
        previous_line = lines[line_no - 1]
    next_line = None
    if line_no < MAX_LEN - 1:
        next_line = lines[line_no + 1]
    for number in numbers:
        is_valid = is_part_number(number, line, previous_line, next_line)
        if is_valid:
            pos, length = number
            number_as_int = int(line[pos : pos + length])
            answer_1 += number_as_int
print(answer_1)

numbers = find_numbers(lines[0])
all_numbers = {line_no: find_numbers(line) for line_no, line in enumerate(lines)}
all_numbers_ordered = [
    (line_no, pos, n) for line_no, numbers in all_numbers.items() for pos, n in numbers
]
to_number_index = -np.ones((MAX_LEN, MAX_LEN), dtype=np.int16)
for number_idx, (line_no, pos, n) in enumerate(all_numbers_ordered):
    for idx in range(pos, pos + n):
        to_number_index[line_no, idx] = number_idx


def get_adjacent(line_no, pos):
    if line_no < 0 or line_no > MAX_LEN - 1 or pos < 0 or pos > MAX_LEN - 1:
        return None
    idx = to_number_index[line_no, pos]
    if idx == -1:
        return None
    return idx


def find_adjacent_numbers(line_no, pos):
    adjacent = [
        get_adjacent(line_no - 1, pos - 1),
        get_adjacent(line_no - 1, pos),
        get_adjacent(line_no - 1, pos + 1),
        get_adjacent(line_no, pos - 1),
        get_adjacent(line_no, pos + 1),
        get_adjacent(line_no + 1, pos - 1),
        get_adjacent(line_no + 1, pos),
        get_adjacent(line_no + 1, pos + 1),
    ]
    adjacent = list(set([x for x in adjacent if x is not None]))
    return adjacent


def get_int(adj):
    l0, p0, n0 = all_numbers_ordered[adj]
    x0 = int(lines[l0][p0 : p0 + n0])
    return x0


# answer_2 is the sum of gear ratios
answer_2 = 0
for line_no in range(MAX_LEN):
    for pos in range(MAX_LEN):
        if lines[line_no][pos] != "*":
            continue
        adjacent = find_adjacent_numbers(line_no, pos)
        if len(adjacent) != 2:
            continue
        answer_2 += get_int(adjacent[0]) * get_int(adjacent[1])
print(answer_2)
