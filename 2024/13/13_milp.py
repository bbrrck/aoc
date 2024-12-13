import re

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

p = r"""Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"""
c = [3, 1]
o = [0, 0]
d = [0, 1e13]
B = [100, np.inf]
t = 0.1
for m in re.findall(p, open("input.txt").read()):
    A, b = (x := np.array(list(map(int, m))))[:4].reshape(2, 2).transpose(), x[4:]
    for k in range(2):
        lc = LinearConstraint(A, (_b := b + d[k]) - t, _b + t)
        f = milp(c=c, constraints=lc, integrality=[1, 1], bounds=Bounds(0, B[k]))
        o[k] += f.fun if f.success else 0
print(int(o[0]))
print(int(o[1]))
