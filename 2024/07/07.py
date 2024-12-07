import sys
from functools import reduce
from operator import add, mul, or_
from pathlib import Path

from tqdm import tqdm

filename = Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else sys.argv[1]

with open(filename) as f:
    data = f.read()  # noqa: F841


def concat(x, y):
    """Concatenate two numbers.

    Operator is used in Part 2.
    """
    return int(str(x) + str(y))


def is_valid_equation(y, xs, i, next_op, running_total, ops):
    """Check if the equation is valid.

    Parameters
    ----------
    y : int
        The target value.
    xs : list of int
        The numbers in the equation.
    i : int
        The index of the current operation in the equation.
    next_op : function
        The function to use to add the next number to the running total.
    running_total : int
        The current running total.
    ops : list of functions
        The functions to use to add the next number to the running total.
        For part 1, ops = [add, mul].
        For part 2, ops = [add, mul, concat].

    Returns
    -------
    bool
        True if there is a combination of ops that combines the xs up to y, False otherwise.
    """
    # If end is reached, check if we have a match
    if i == len(xs) - 1:
        return running_total == y
    # Update the running total
    running_total = next_op(running_total, xs[i + 1])
    # If the running total is too big, return early
    if running_total > y:
        return False
    # Check the next operation
    return reduce(
        or_,
        (is_valid_equation(y, xs, i + 1, op, running_total, ops) for op in ops),
    )


# Parse input data
equations = [line.split(": ") for line in data.splitlines()]
results = []
numbers = []
for y, xs in equations:
    results.append(int(y))
    numbers.append(list(map(int, xs.split(" "))))

# Initialize
ops_1 = [add, mul]
ops_2 = [add, mul, concat]
answer_1 = 0
answer_2 = 0

# Loop over all equations
for y, xs in tqdm(list(zip(results, numbers))):
    matched_1 = reduce(
        or_,
        (is_valid_equation(y, xs, 0, op, xs[0], ops_1) for op in ops_1),
    )
    matched_2 = reduce(
        or_,
        (is_valid_equation(y, xs, 0, op, xs[0], ops_2) for op in ops_2),
    )
    # Update totals if a match was found
    if matched_1:
        answer_1 += y
    if matched_2:
        answer_2 += y
print(answer_1)
print(answer_2)
