from dataclasses import dataclass
import math
from pprint import pprint
import re

import numpy as np
from utils import IntVec2D


@dataclass
class Machine:
    b1: IntVec2D
    b2: IntVec2D
    prize: IntVec2D


button_re = re.compile(r"Button \w: X\+(\d+), Y\+(\d+)")
prize_re = re.compile(r"Prize: X=(\d+), Y=(\d+)")


def parse_machines(inp: str) -> list[Machine]:
    res: list[Machine] = []
    paragraphs = inp.split("\n\n")
    for p in paragraphs:
        l1, l2, l3 = p.splitlines()
        b1_match = button_re.match(l1)
        b2_match = button_re.match(l2)
        prize_match = prize_re.match(l3)
        assert all(
            m is not None for m in (b1_match, b2_match, prize_match)
        ), f"{p}; {b1_match}, {b2_match}, {prize_match}"
        res.append(
            Machine(
                b1=IntVec2D(x=int(b1_match.group(1)), y=int(b1_match.group(2))),
                b2=IntVec2D(x=int(b2_match.group(1)), y=int(b2_match.group(2))),
                prize=IntVec2D(x=int(prize_match.group(1)), y=int(prize_match.group(2))),
            )
        )

    return res


def count_tokens(machines: list[Machine]) -> int:
    total = 0
    for m in machines:
        emat = np.array(
            [
                [m.b1 * m.b1, m.b1 * m.b2],
                [m.b1 * m.b2, m.b2 * m.b2],
            ]
        )
        # NOTE: will fail on colinear b1 and b2, but they're not in the input
        components = np.linalg.inv(emat) @ np.array([m.prize * m.b1, m.prize * m.b2]).T
        press_1, press_2 = round(components[0]), round(components[1])
        if m.prize == press_1 * m.b1 + press_2 * m.b2:
            total += press_1 * 3 + press_2
    return total


def part_1(inp: str, debug: bool):
    print(count_tokens(parse_machines(inp)))


def part_2(inp: str, debug: bool):
    machines = parse_machines(inp)
    conversion_error = IntVec2D(10000000000000, 10000000000000)
    for m in machines:
        m.prize = m.prize + conversion_error
    print(count_tokens(machines))
