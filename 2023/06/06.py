with open("input.txt", "r") as f:
    TIME, DIST = [x.split(":")[1].strip(" ") for x in f.read().strip("\n").split("\n")]

#### Part 1
TIME_1 = [int(x) for x in TIME.split(" ") if x != ""]
DIST_1 = [int(x) for x in DIST.split(" ") if x != ""]
answer_1 = 1
for t_total, dist_target in zip(TIME_1, DIST_1):
    n_winning = 0
    for speed in range(t_total):
        t_remaining = t_total - speed
        traveled = t_remaining * speed
        winning = traveled > dist_target
        n_winning += int(winning)
    answer_1 *= n_winning
print(answer_1)

#### Part 2
TIME_2 = int(TIME.replace(" ", ""))
DIST_2 = int(DIST.replace(" ", ""))
left = 0
right = TIME_2 // 2
depth = 0
while right - left > 1:
    mid = (left + right) // 2
    if (TIME_2 - mid) * mid > DIST_2:
        right = mid
    else:
        left = mid
answer_2 = TIME_2 - 2 * right + 1
print(answer_2)
