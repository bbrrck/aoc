import os
import sys
from functools import partial
from multiprocessing import Pool
from operator import add, mul
from pathlib import Path
from typing import Callable

from tqdm import tqdm


def concat(x, y):
    """Concatenate two numbers.

    Operator is used in Part 2.
    """
    return int(str(x) + str(y))


def validate_equation(
    equation: tuple[int, list[int]],
    ops: list,
    depth: int = 0,
    next_op: Callable | None = None,
    running_total: int | None = None,
) -> int:
    """Check if the equation is valid.

    Parameters
    ----------
    equation : tuple[int, list[int]]
        The equation to check.
        - equation[0] is the target value.
        - equation[1] is the list of numbers that should be added/multiplied/concatenated.
    ops : list
        Possible operators to use to add the next number to the running total.
        For part 1, ops = [add, mul].
        For part 2, ops = [add, mul, concat].
    depth : int
        The index of the current x that is being added to the running total.
    next_op : function
        The function to use to add the next number to the running total.
    running_total : int
        The current running total.

    Returns
    -------
    int
        target value (equation[0]) if there exists a combination of ops
        that makes the equation valid; 0 otherwise.
    """
    y, xs = equation

    # Start
    if next_op is None:
        # Initialize the combination
        running_total = xs[0]

    # End
    elif depth == len(xs):
        # If end is reached, check if we have a match
        return y if running_total == y else 0

    # Middle
    else:
        # Update the running total
        running_total = next_op(running_total, xs[depth])
        # If the running total is too big, return early
        if running_total > y:
            return 0

    # Recursion: check the next operation
    return max(
        [
            validate_equation(
                equation=equation,
                ops=ops,
                next_op=op,
                depth=depth + 1,
                running_total=running_total,
            )
            for op in ops
        ]
    )


# Read and parse input data
filename = Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else sys.argv[1]
with open(filename) as f:
    equations = [
        (int((eq := line.split(": "))[0]), list(map(int, eq[1].split(" "))))
        for line in f.read().splitlines()
    ]

# Process using multiprocessing
print(f"CPU count: {os.cpu_count()}")
ops_1 = (add, mul)
ops_2 = (add, mul, concat)
with Pool(os.cpu_count()) as pool:
    answer_1 = list(tqdm(pool.imap(partial(validate_equation, ops=ops_1), equations)))
    answer_2 = list(tqdm(pool.imap(partial(validate_equation, ops=ops_2), equations)))
print(sum(answer_1))
print(sum(answer_2))
