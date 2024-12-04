from typing import Literal
from utils import Map2D


def part_1(inp: str, debug: bool):
    map = Map2D[str].parse(inp)
    xmas_count = 0
    for i, j, letter in map.iter_cells():
        if letter != "X":
            continue
        for di, dj in (
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
            (1, 1),
            (1, -1),
            (-1, -1),
            (-1, 1),
        ):
            for step, next_letter in zip((1, 2, 3), ("M", "A", "S")):
                i_letter = i + di * step
                j_letter = j + dj * step
                if map.at(i_letter, j_letter) != next_letter:
                    break
            else:
                xmas_count += 1

    print(xmas_count)


def part_2(inp: str, debug: bool):
    mat = Map2D[str].parse(inp)
    x_mas_count = 0
    for i, j, letter in mat.iter_cells():
        if letter != "A":
            continue
        for ms_rotation in ("MMSS", "MSMS", "SSMM", "SMSM"):
            for (di, dj), letter in zip(
                (
                    (-1, -1),
                    (1, -1),
                    (-1, 1),
                    (1, 1),
                ),
                ms_rotation,
            ):
                i_l = i + di
                j_l = j + dj
                if mat.at(i_l, j_l) != letter:
                    break
            else:
                x_mas_count += 1
    print(x_mas_count)
