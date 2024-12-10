from functools import lru_cache
from utils import Map2D


STEPS = (
    (-1, 0),
    (1, 0),
    (0, 1),
    (0, -1),
)


def part_1(inp: str, debug: bool):
    map = Map2D.parse(inp, char_parser=lambda ch: int(ch) if ch != "." else 100)

    @lru_cache
    def reachable_highs(i: int, j: int) -> set[tuple[int, int]]:
        elevation = map.at(i, j)
        if elevation is None:
            return set()
        elif elevation == 9:
            return {(i, j)}
        else:
            res = set()
            for di, dj in STEPS:
                if map.at(i + di, j + dj) == elevation + 1:
                    res.update(reachable_highs(i + di, j + dj))
            return res

    total_score = 0
    for i, j, elevation in map.iter_cells():
        if elevation == 0:
            total_score += len(reachable_highs(i, j))

    print(total_score)


def part_2(inp: str, debug: bool):
    map = Map2D.parse(inp, char_parser=lambda ch: int(ch) if ch != "." else 100)

    @lru_cache
    def trails_from(i: int, j: int) -> int:
        elevation = map.at(i, j)
        if elevation is None:
            return 0
        elif elevation == 9:
            return 1
        else:
            return sum(
                trails_from(i + di, j + dj)
                for di, dj in STEPS
                if map.at(i + di, j + dj) == elevation + 1
            )

    total_rating = 0
    for i, j, elevation in map.iter_cells():
        if elevation == 0:
            total_rating += trails_from(i, j)

    print(total_rating)
