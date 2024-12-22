import sys
from collections import defaultdict
from pathlib import Path

from tqdm import tqdm


BASE = 16777216
N_SECRETS = 2000


def get_secret(x: int) -> int:
    x = ((x * 64) ^ x) % BASE
    x = ((x // 32) ^ x) % BASE
    x = ((x * 2048) ^ x) % BASE
    return x


filename = (
    Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else Path(sys.argv[1])
)
with open(filename) as f:
    initial_secrets = map(int, f.read().strip("\n").split("\n"))


answer_1 = 0
n_bananas = defaultdict(int)
for secret in tqdm(initial_secrets):
    price_prev = secret % 10
    d0, d1, d2, d3 = None, None, None, None
    keys = set()
    for _ in range(N_SECRETS):
        secret = get_secret(secret)
        price = secret % 10
        d0, d1, d2, d3, price_prev = d1, d2, d3, price - price_prev, price
        key = (d0, d1, d2, d3)
        if any(map(lambda x: x is None, key)):
            continue
        if key in keys:
            continue
        n_bananas[key] += price
        keys.add(key)
    answer_1 += secret
answer_2 = max(n_bananas.values())

print(answer_1)
print(answer_2)
