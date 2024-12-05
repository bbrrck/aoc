dirmap = {"0": "R", "1": "D", "2": "L", "3": "U"}

with open("input.txt") as f:
    data = f.read().strip("\n").split("\n")
    data = [line.split(" ") for line in data]
    data = [(direction, int(steps), color[2:-1]) for direction, steps, color in data]
    # part 1
    dirs1 = [x[0] for x in data]
    dist1 = [x[1] for x in data]
    # part 2
    dirs2 = [dirmap[x[2][5]] for x in data]
    dist2 = [int(x[2][:5], 16) for x in data]


def area(directions, distances):
    # get polygon boundary
    # also keep track of boundary length (total_steps)
    last = [0, 0]
    boundary = [last.copy()]
    total_steps = 0
    for steps, direction in zip(distances, directions):
        if direction == "R":
            last[0] += steps
        if direction == "L":
            last[0] -= steps
        if direction == "U":
            last[1] -= steps
        if direction == "D":
            last[1] += steps
        total_steps += steps
        boundary.append(last.copy())

    # compute inner area using the triangle formula
    # https://en.wikipedia.org/wiki/Shoelace_formula
    inner = 0
    for i in range(len(boundary) - 1):
        x0, y0 = boundary[i]
        x1, y1 = boundary[i + 1]
        inner += x0 * y1 - x1 * y0

    # not sure why this formula works, but it does
    return int(inner / 2 + total_steps / 2 + 1)


answer_1 = area(dirs1, dist1)
answer_2 = area(dirs2, dist2)

print(answer_1)
print(answer_2)
