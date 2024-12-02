import numpy as np


def check_levels(levels: np.ndarray) -> bool:
    diffs = np.diff(levels)
    diffs_abs = np.abs(diffs)
    if not np.all(np.logical_and(diffs_abs >= 1, diffs_abs <= 3)):
        return False
    if not (np.all(diffs > 0) or np.all(diffs < 0)):
        return False
    return True


def part_1(inp: str, debug: bool):
    res = 0
    for line in inp.splitlines():
        levels = np.fromstring(line, dtype=int, sep=" ")
        res += int(check_levels(levels))
    print(res)


def part_2(inp: str, debug: bool):
    res = 0
    for line in inp.splitlines():
        levels = np.fromstring(line, dtype=int, sep=" ")
        if check_levels(levels):
            res += 1
        else:
            for missing_i in range(len(levels)):
                if check_levels(np.delete(levels, missing_i)):
                    res += 1
                    break
    print(res)
