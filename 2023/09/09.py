import numpy as np

with open("input.txt", "r") as f:
    lines = [
        [int(x) for x in line.split(" ")] for line in f.read().strip("\n").split("\n")
    ]

answer_1 = 0
for numbers in lines:
    k = len(numbers)
    M = np.zeros([k + 1, k + 1], dtype=np.int32)
    M[0, :k] = numbers
    last = 0
    for r in range(0, k - 1):
        s = np.ediff1d(M[r, : k - r])
        last = r
        if s.sum() == 0:
            break
        M[r + 1, : k - r - 1] = s
        last = r + 1
    else:
        raise RuntimeError(f"NEVER STOPPED: {numbers}")
    for r in reversed(range(last + 1)):
        M[r, k - r] = M[r, k - r - 1] + M[r + 1, k - r - 1]
    answer_1 += M[0, k]
print(answer_1)

answer_2 = 0
for numbers in lines:
    k = len(numbers)
    M = np.zeros([k + 1, k + 1], dtype=np.int32)
    M[0, 1 : k + 1] = numbers
    last = 0
    for r in range(0, k - 1):
        s = np.ediff1d(M[r, r + 1 :])
        last = r
        if s.sum() == 0:
            break
        M[r + 1, r + 2 :] = s
        last = r + 1
    else:
        raise RuntimeError(f"NEVER STOPPED: {numbers}")
    for r in reversed(range(last + 1)):
        M[r, r] = M[r, r + 1] - M[r + 1, r + 1]
    answer_2 += M[0, 0]
print(answer_2)
