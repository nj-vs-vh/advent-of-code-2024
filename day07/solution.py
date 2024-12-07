import itertools
import operator
from typing import Callable

Operator = Callable[[int, int], int]

def calibration_result(line: str, operators: list[Operator]) -> int:
    target, nums = line.split(":")
    target = int(target)
    nums = list(map(int, nums.split()))
    subresults: set[int] = {op(nums[0], nums[1]) for op in operators}
    for num in nums[2:]:
        new_subresults = set()
        for prev in subresults:
            for op in operators:
                new_subres = op(prev, num)
                if new_subres <= target:
                    new_subresults.add(new_subres)
        subresults = new_subresults
    return target if target in subresults else 0


def part_1(inp: str, debug: bool):
    ans = 0
    for line in inp.splitlines():
        ans += calibration_result(line, operators=[operator.add, operator.mul])
    print(ans)


def concatenate(a: int, b: int) -> int:
    return int(str(a) + str(b))


def part_2(inp: str, debug: bool):
    ans = 0
    for line in inp.splitlines():
        ans += calibration_result(line, operators=[operator.add, operator.mul, concatenate])
    print(ans)
