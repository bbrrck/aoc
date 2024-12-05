import re

with open("input.txt") as f:
    workflows, parts = f.read().strip("\n").split("\n\n")
    parts = re.findall(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}", parts)
    parts = [(int(x), int(m), int(a), int(s)) for x, m, a, s in parts]

W = {}
for w in workflows.split("\n"):
    name, definition = w[:-1].split("{")
    definition = definition.split(",")
    instructions = []
    for d in definition:
        if ":" in d:
            x, o = d.split(":")
            instructions.append(
                {
                    "cat": x[0],
                    "op": x[1],
                    "val": int(x[2:]),
                    "cond": x,
                    "out": o,
                }
            )
        else:
            instructions.append({"out": d})
    W[name] = instructions


def evaluate(workflow_name, x, m, a, s):
    # print(workflow_name)
    for step in W[workflow_name]:
        outcome = step["out"]
        if "cond" in step:
            condition = step["cond"]
            if not eval(condition):
                continue
        if outcome == "A":
            return True
        if outcome == "R":
            return False
        return evaluate(outcome, x, m, a, s)


answer_1 = 0
for idx, (x, m, a, s) in enumerate(parts):
    # print("-" * 80)
    # print(idx)
    # print(x, m, a, s)
    accepted = evaluate("in", x, m, a, s)
    if accepted:
        answer_1 += sum([x, m, a, s])
print(answer_1)  # CORRECT: 325952


def split(interval, operation, value):
    if operation == ">":
        is_false = range(interval.start, value + 1)
        # value is included in "false"
        is_true = range(value + 1, interval.stop)
        return is_true, is_false

    if operation == "<":
        is_true = range(interval.start, value)
        # value is included in "false"
        is_false = range(value, interval.stop)
        return is_true, is_false

    raise RuntimeError(f"Invalid operation: {operation}")


results = []


def evaluate(workflow_name, x, m, a, s):
    if len(x) < 0:
        raise RuntimeError(f"Invalid x range: {x}")
    if len(m) < 0:
        raise RuntimeError(f"Invalid m range: {m}")
    if len(a) < 0:
        raise RuntimeError(f"Invalid a range: {a}")
    if len(s) < 0:
        raise RuntimeError(f"Invalid s range: {s}")
    if not x:
        return
    if not m:
        return
    if not a:
        return
    if not s:
        return
    global results
    # print(f"{workflow_name = }")
    for step in W[workflow_name]:
        # if "cond" in step:
        #     print(f"{step['cond']} : {step['out']}")
        # else:
        #     print(f"--> {step['out']}")
        outcome = step["out"]
        if "cond" in step:
            category = step["cat"]
            operation = step["op"]
            value = step["val"]
            if category == "x":
                x1, x0 = split(x, operation, value)
                m1, m0 = m, m
                a1, a0 = a, a
                s1, s0 = s, s
                # print("splitting x")
                # print(f"{x1 = }")
                # print(f"{x0 = }")
            elif category == "m":
                x1, x0 = x, x
                m1, m0 = split(m, operation, value)
                a1, a0 = a, a
                s1, s0 = s, s
                # print("splitting m")
                # print(f"{m1 = }")
                # print(f"{m0 = }")
            elif category == "a":
                x1, x0 = x, x
                m1, m0 = m, m
                a1, a0 = split(a, operation, value)
                s1, s0 = s, s
                # print("splitting a")
                # print(f"{a1 = }")
                # print(f"{a0 = }")
            elif category == "s":
                x1, x0 = x, x
                m1, m0 = m, m
                a1, a0 = a, a
                s1, s0 = split(s, operation, value)
                # print("splitting s")
                # print(f"{s1 = }")
                # print(f"{s0 = }")
            else:
                raise RuntimeError(f"Invalid category: {category}")
            # The part that was true should be returned, or recursed
            if outcome == "A":
                results.append((x1, m1, a1, s1, True))
            elif outcome == "R":
                results.append((x1, m1, a1, s1, False))
            else:
                evaluate(outcome, x1, m1, a1, s1)
            # The part that was false should continue in the loop
            x = x0
            m = m0
            a = a0
            s = s0
        else:
            # there is no condition, just return the output
            if outcome == "A":
                results.append((x, m, a, s, True))
            elif outcome == "R":
                results.append((x, m, a, s, False))
            else:
                evaluate(outcome, x, m, a, s)


# all values 1 to a maximum of 4000
limit = 4001
X = range(1, limit)
M = range(1, limit)
A = range(1, limit)
S = range(1, limit)
results = []
evaluate("in", X, M, A, S)

answer_2 = 0
for x, m, a, s, valid in results:
    if not valid:
        continue
    answer_2 += len(x) * len(m) * len(a) * len(s)
print(answer_2)
