#### Part 1

import random
from itertools import combinations
from multiprocessing import Pool

import numpy as np
import scipy
from sympy import Eq, solve, symbols
from tqdm.auto import tqdm

# filename = "example.txt"
# MIN = 7
# MAX = 27

filename = "input.txt"
MIN = 200000000000000
MAX = 400000000000000


with open(filename) as f:
    data = f.read().strip("\n").split("\n")

pos = [[int(i) for i in line.split(" @ ")[0].split(", ")] for line in data]
vel = [[int(i) for i in line.split(" @ ")[1].split(", ")] for line in data]
s, t = symbols("s t")

#### Part 1
answer_1 = 0


def solve_one(p1, v1, p2, v2):
    p1x, p1y = p1[:2]
    p2x, p2y = p2[:2]
    v1x, v1y = v1[:2]
    v2x, v2y = v2[:2]
    eq1 = Eq(p1x + v1x * s, p2x + v2x * t)
    eq2 = Eq(p1y + v1y * s, p2y + v2y * t)
    params = solve((eq1, eq2), (s, t))
    if not params:
        return 0
    ss = float(params[s])
    tt = float(params[t])
    if ss < 0:
        return 0
    if tt < 0:
        return 0
    x = p1x + v1x * ss
    y = p1y + v1y * ss
    if x < MIN or x > MAX or y < MIN or y > MAX:
        return 0
    return 1


def solve_one_wrapper(args):
    p1, v1 = args[0]
    p2, v2 = args[1]
    return solve_one(p1, v1, p2, v2)


with Pool() as pool:
    answer_1 = sum(pool.map(solve_one_wrapper, list(combinations(zip(pos, vel), 2))))
print(answer_1)

#### Part 2

# P1 + t1 * V1 = P0 + t1 * V0
# P2 + t2 * V2 = P0 + t2 * V0
# P3 + t3 * V3 = P0 + t3 * V0
# ...
# Pn + tn * Vn = P0 + tn * V0

# px1 + t1 * vx1 = px0 + t1 * vx0
# ...
# pxn + tn * vxn = px0 + tn * vx0

# (px0 - px1) + t1 * (vx0 - vx1) = 0
# (py0 - py1) + t1 * (vy0 - vy1) = 0
# (pz0 - pz1) + t1 * (vz0 - vz1) = 0
# (px0 - px2) + t2 * (vx0 - vx2) = 0
# (py0 - py2) + t2 * (vy0 - vy2) = 0
# (pz0 - pz2) + t2 * (vz0 - vz2) = 0
# ...
# ...
# ...
# (px0 - pxn) + tn * (vx0 - vxn) = 0
# (py0 - pyn) + tn * (vy0 - vyn) = 0
# (pz0 - pzn) + tn * (vz0 - vzn) = 0

# Number of equations: 3*n
# Number of DoFs: n + 3

with open("input.txt") as f:
    data = f.read().strip("\n").split("\n")

pos = [[int(i) for i in line.split(" @ ")[0].split(", ")] for line in data]
vel = [[int(i) for i in line.split(" @ ")[1].split(", ")] for line in data]
P0 = np.array(pos, dtype=np.int64)
V = np.array(vel, dtype=np.int64)
centroid = P0.mean(axis=0)
centroid = np.round(centroid).astype(int)
s = P0.max() - P0.min()
P = P0
# P = P0 - centroid
# P = P0 / s
# P.mean(axis=0)
K = 6 + P.shape[0]


def fun(params):
    px0, py0, pz0 = params[:3]
    vx0, vy0, vz0 = params[3:6]
    t = params[6:]
    f = []
    fprime = []
    for k, tk in enumerate(t):
        pxk = P[k, 0]
        pyk = P[k, 1]
        pzk = P[k, 2]
        vxk = V[k, 0]
        vyk = V[k, 1]
        vzk = V[k, 2]
        f.append((px0 - pxk) + tk * (vx0 - vxk))
        g = [0] * K
        g[0] = 1
        g[3] = tk
        g[6 + k] = vx0 - vxk
        fprime.append(g)

        f.append((py0 - pyk) + tk * (vy0 - vyk))
        g = [0] * K
        g[1] = 1
        g[4] = tk
        g[6 + k] = vy0 - vyk
        fprime.append(g)

        f.append((pz0 - pzk) + tk * (vz0 - vzk))
        g = [0] * K
        g[2] = 1
        g[5] = tk
        g[6 + k] = vz0 - vzk
        fprime.append(g)

    return f
    # return f, fprime


# x0 = [0] * (6 + len(pos))
x0 = [random.randint(0, 1_000_000_000_000_000) for _ in range(6 + len(pos))]
# x0 = [24, 13, 10, -3, 1, 2, 5, 3, 4, 6, 1]
# print(len(x0), x0)

result = scipy.optimize.root(fun=fun, x0=x0, jac=False, method="lm")  # , tol=0.01)
# result = scipy.optimize.root(fun=fun, x0=x0, jac=True, method="lm") #, tol=0.01)
# result

# +
# fun(result.x.round()) # SHOULD BE ALL ZEROS
# -

answer_2 = int(result.x[:3].sum())
print(answer_2)
