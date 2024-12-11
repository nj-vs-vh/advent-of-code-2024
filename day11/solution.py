def after_blink(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    stone_str = str(stone)
    if len(stone_str) % 2 == 0:
        split_at = len(stone_str) // 2
        return [
            int(stone_str[:split_at]),
            int(stone_str[split_at:]),
        ]
    else:
        return [stone * 2024]


def blink(stones: list[int]) -> None:
    i = 0
    while i < len(stones):
        stone = stones[i]
        new = after_blink(stone)
        stones[i] = new[0]
        if len(new) == 2:
            stones.insert(i, new[1])
        i += len(new)


CACHE = dict[int, list[int]]()


def multiplicities_at_depths(stone: int, depth: int) -> list[int]:
    if depth == 0:
        return [1]

    cached = CACHE.get(stone)
    if cached is not None and len(cached) >= depth:
        return cached

    substones = after_blink(stone)
    branch_multiplicities = [multiplicities_at_depths(s, depth=depth - 1) for s in substones]
    res = [1]
    res.extend(map(sum, zip(*branch_multiplicities)))
    CACHE[stone] = res
    return res


def part_1(inp: str, debug: bool):
    stones = list(map(int, inp.split()))
    print(sum(multiplicities_at_depths(s, depth=26)[-1] for s in stones))


def part_2(inp: str, debug: bool):
    stones = list(map(int, inp.split()))
    print(sum(multiplicities_at_depths(s, depth=76)[-1] for s in stones))
