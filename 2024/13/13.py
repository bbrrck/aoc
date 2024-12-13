import re
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

filename = Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else sys.argv[1]

with open(filename) as f:
    data = f.read()


machines = re.findall(
    r"""Button A: X\+(\d+), Y\+(\d+)
Button B: X\+(\d+), Y\+(\d+)
Prize: X=(\d+), Y=(\d+)""",
    data,
    re.MULTILINE,
)

COST_A, COST_B = 3, 1

# Problem:
#   Minimize
#     3 * wa + 1 * wb
#   Such that
#     wa * xa + wb * xb = xp
#     wa * ya + wb * yb = yp
#   Example:
#     xa = 94, ya = 34
#     xb = 22, yb = 67
#     xp = 8400, yp = 5400
#   --> wa = 80, wb = 40

c = np.array([COST_A, COST_B])
integrality = [1, 1]
answer_1 = 0
answer_2a = 0
answer_2b = 0
for machine in machines:
    xa, ya, xb, yb, xp, yp = map(int, machine)
    A = np.array([[xa, xb], [ya, yb]])
    b1 = np.array([xp, yp])
    b2 = b1 + 10000000000000

    # Part 1 via mixed-integer programming --> this works fine
    out_1 = milp(
        c=c,
        integrality=[1, 1],
        constraints=LinearConstraint(A=A, lb=b1, ub=b1),
        bounds=Bounds(lb=0, ub=100),
    )
    if out_1.success:
        answer_1 += out_1.fun

    # Part 2 via mixed-integer programming --> this does not give the correct answer
    out_2 = milp(
        c=[COST_A, COST_B],
        integrality=[1, 1],
        constraints=LinearConstraint(A=A, lb=b2, ub=b2),
        bounds=Bounds(lb=0, ub=np.inf),
    )
    if out_2.success:
        answer_2a += out_2.fun

    # Part 2 via naive matrix inversion
    x = np.matmul(np.linalg.inv(A), b2)
    # check if x has integer elements
    if np.abs(x - np.round(x)).sum() > 0.01:  # This threshold works for some reason
        continue
    answer_2b += np.dot(c, np.round(x))

print(int(answer_1))
print(int(answer_2b))
