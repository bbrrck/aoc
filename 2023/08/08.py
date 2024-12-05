import math

with open("input.txt", "r") as f:
    instr, raw_map = f.read().strip("\n").split("\n\n")
    raw_map = [x for x in raw_map.split("\n")]

#### Prepare maps
maps = {"L": {}, "R": {}}
for line in raw_map:
    src, dest = line.split(" = ")
    left, right = dest.split(", ")
    maps["L"][src] = left.strip("(")
    maps["R"][src] = right.strip(")")

#### Part 1
pos = "AAA"
answer_1 = 0
while pos != "ZZZ":
    key = instr[answer_1 % len(instr)]
    pos = maps[key][pos]
    answer_1 += 1
print(answer_1)

#### Part 2
start = list(filter(lambda x: x[2] == "A", maps["L"].keys()))
finish = []
steps = []
for pos in start:
    answer_1 = 0
    while pos[2] != "Z":
        key = instr[answer_1 % len(instr)]
        pos = maps[key][pos]
        answer_1 += 1
    steps.append(answer_1)
    finish.append(pos)
answer_2 = math.lcm(*steps)
print(answer_2)
