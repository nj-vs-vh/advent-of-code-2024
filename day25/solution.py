import itertools
import numpy as np


def part_1(inp: str, debug: bool):
    keys = []
    locks = []
    for p in inp.split("\n\n"):
        vals = np.array([[1 if ch == "#" else 0 for ch in l] for l in p.splitlines()])
        if vals[0, 0] == 1:
            locks.append(vals.sum(axis=0) - 1)
        else:
            keys.append(vals.sum(axis=0) - 1)

    res = 0
    for k, l in itertools.product(keys, locks):
        res += int(np.all(k + l < 6))
    print(res)


def part_2(inp: str, debug: bool):
    pass
