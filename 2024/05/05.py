import sys
from copy import deepcopy
from pathlib import Path

filename = Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else sys.argv[1]

with open(filename) as f:
    data = f.read()

all_rules, all_updates = data.strip("\n").split("\n\n")
all_rules = [tuple(map(int, rule.split("|"))) for rule in all_rules.split("\n")]
all_updates = [list(map(int, update.split(","))) for update in all_updates.split("\n")]


def get_middle_element(x: list[int]) -> int:
    return x[len(x) // 2]


def get_rules_for_update(update: list):
    return [rule for rule in all_rules if rule[0] in update and rule[1] in update]


def is_rule_respected(update, rule):
    return update.index(rule[0]) < update.index(rule[1])


def is_valid(update: list):
    rules = get_rules_for_update(update)
    return all(map(lambda rule: is_rule_respected(update, rule), rules))


answer_1 = sum(map(get_middle_element, filter(is_valid, all_updates)))
print(answer_1)

MAX_ITER = 1000
invalid = deepcopy(list(filter(lambda x: not is_valid(x), all_updates)))
for update in invalid:
    update_rules = get_rules_for_update(update)
    niter = 0
    while not is_valid(update):
        niter += 1
        if niter > MAX_ITER:
            raise RuntimeError(f"Maximum number of iterations reached [{MAX_ITER}]")
        for rule in update_rules:
            if is_rule_respected(update, rule):
                continue
            i, j = map(update.index, rule)
            update[i], update[j] = update[j], update[i]
answer_2 = sum(map(get_middle_element, invalid))
print(answer_2)
