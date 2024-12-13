import re
import numpy as np

p = r"""Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"""
c = [3, 1]
o = [0, 0]
d = [0, 1e13]
for m in re.findall(p, open("input.txt").read()):
    A, b = (x := np.array(list(map(int, m))))[:4].reshape(2, 2).transpose(), x[4:]
    for k in range(2):
        x = np.linalg.solve(A, b + d[k])
        if np.abs(x - np.round(x)).sum() < 0.01:
            o[k] += np.dot(c, np.round(x))
print(int(o[0]))
print(int(o[1]))
