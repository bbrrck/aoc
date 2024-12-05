with open("input.txt") as f:
    parts = f.read().strip("\n").replace("\n", "").split(",")


def myhash(X):
    k = 0
    for x in X:
        k = ((k + ord(x)) * 17) % 256
    return k


#### Part 1
answer_1 = sum([myhash(part) for part in parts])
print(answer_1)

#### Part 2
boxes = [dict() for _ in range(256)]
for part in parts:
    if "=" in part:
        operation = "="
        label, focal_length = part.split("=")
        box_id = myhash(label)
        boxes[box_id][label] = int(focal_length)
    else:
        operation = "-"
        label = part[:-1]
        box_id = myhash(label)
        if label in boxes[box_id]:
            del boxes[box_id][label]
answer_2 = 0
for box_id, box in enumerate(boxes):
    for slot_id, focal_length in enumerate(box.values()):
        answer_2 += (box_id + 1) * (slot_id + 1) * focal_length
print(answer_2)
