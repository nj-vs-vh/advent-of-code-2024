import collections
import itertools

from utils import sliding_window


PRUNE_BITS = 2**24 - 1


def rng_next(curr: int) -> int:
    curr = (curr ^ (curr << 6)) & PRUNE_BITS
    curr = (curr ^ (curr >> 5)) & PRUNE_BITS
    curr = (curr ^ (curr << 11)) & PRUNE_BITS
    return curr


def rng_forward(seed: int, steps: int) -> int:
    for _ in range(steps):
        seed = rng_next(seed)
    return seed


def part_1(inp: str, debug: bool):
    res = 0
    for seed_str in inp.splitlines():
        seed = int(seed_str)
        res += rng_forward(seed, 2000)
    print(res)


def part_2(inp: str, debug: bool):
    bananas_bought_total: dict[tuple[int, ...], int] = collections.defaultdict(lambda: 0)
    for seed in inp.splitlines():
        n = int(seed)
        prices = [n % 10]
        for _ in range(2000):
            n = rng_next(n)
            prices.append(n % 10)

        diffs = [p2 - p1 for p1, p2 in itertools.pairwise(prices)]
        bananas_bought: dict[tuple[int, ...], int] = dict()
        for i, diffseq in enumerate(sliding_window(diffs, n=4)):
            if diffseq in bananas_bought:
                continue
            bananas_bought[diffseq] = prices[i + 4]

        for ds, b in bananas_bought.items():
            bananas_bought_total[ds] += b

    best = max(bananas_bought_total.values())
    print([k for k, v in bananas_bought_total.items() if v == best])
    print(best)
