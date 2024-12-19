import collections
from functools import lru_cache


def parse(inp: str) -> tuple[dict[int, set[str]], list[str]]:
    towel_line, patterns = inp.split("\n\n")
    towel_lib: dict[int, set[str]] = collections.defaultdict(set)
    for towel in towel_line.split(", "):
        towel_lib[len(towel)].add(towel)
    return towel_lib, patterns.splitlines()


def is_possible(pattern: str, towel_lib: dict[int, set[str]]) -> bool:
    if not pattern:
        return True

    max_prefix_len = min(max(towel_lib.keys()), len(pattern))
    for prefix_len in range(1, max_prefix_len + 1):
        prefix = pattern[:prefix_len]
        for towel in towel_lib.get(prefix_len, []):
            if towel == prefix:
                if is_possible(pattern[prefix_len:], towel_lib):
                    return True

    return False


def part_1(inp: str, debug: bool):
    towel_lib, patterns = parse(inp)
    answer = 0
    for pattern in patterns:
        res = is_possible(pattern, towel_lib)
        print(f"{pattern} = {res}")
        answer += int(res)
    print(answer)


def part_2(inp: str, debug: bool):
    towel_lib, patterns = parse(inp)

    @lru_cache
    def count_arrangements(pattern: str) -> int:
        if not pattern:
            return 1

        max_prefix_len = min(max(towel_lib.keys()), len(pattern))
        res = 0
        for prefix_len in range(1, max_prefix_len + 1):
            prefix = pattern[:prefix_len]
            for towel in towel_lib.get(prefix_len, []):
                if towel == prefix:
                    res += count_arrangements(pattern[prefix_len:])

        return res

    answer = 0
    for pattern in patterns:
        answer += count_arrangements(pattern)
    print(answer)
