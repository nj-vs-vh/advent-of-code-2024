import collections
import numpy as np


def part_1(inp: str, debug: bool):
    arr = np.array([[int(v) for v in l.split()] for l in inp.splitlines()])
    arr.sort(axis=0)
    print(np.sum(np.abs(np.diff(arr, axis=1))))


def part_2(inp: str, debug: bool):
    arr = np.array([[int(v) for v in l.split()] for l in inp.splitlines()])
    first = arr[:, 0]
    second = arr[:, 1]
    second_counts = collections.Counter(second)
    print(sum(
        f * second_counts.get(f, 0) for f in first
    ))
