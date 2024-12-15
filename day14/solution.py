from dataclasses import dataclass
import functools
import itertools
from operator import mul
import operator
import re
from utils import IntVec2D, Map2D


@dataclass
class Robot:
    r: IntVec2D
    v: IntVec2D


int_vec_re = re.compile(r"\w=(-?\d+),(-?\d+)")


def parse(inp: str) -> list[Robot]:
    res: list[Robot] = []
    for line in inp.splitlines():
        r_str, v_str = line.split(" ")
        r_match = int_vec_re.match(r_str)
        assert r_match is not None
        v_match = int_vec_re.match(v_str)
        assert v_match is not None
        res.append(
            Robot(
                r=IntVec2D(
                    x=int(r_match.group(1)),
                    y=int(r_match.group(2)),
                ),
                v=IntVec2D(
                    x=int(v_match.group(1)),
                    y=int(v_match.group(2)),
                ),
            )
        )
    return res


def part_1(inp: str, debug: bool):
    steps = 100
    w, h = 101, 103
    x_mid = w // 2
    y_mid = h // 2
    quadrant_counts = {
        (1, 1): 0,
        (1, 0): 0,
        (0, 1): 0,
        (0, 0): 0,
    }
    for robot in parse(inp):
        location = robot.r + steps * robot.v
        x = location[0] % w
        y = location[1] % h
        if x == x_mid or y == y_mid:
            continue
        quadrant_counts[(x > x_mid, y > y_mid)] += 1

    print(functools.reduce(operator.mul, quadrant_counts.values(), 1))


def part_2(inp: str, debug: bool):
    robots = parse(inp)
    for steps in itertools.count():
        if (steps - 50) % 103 == 0 and (steps - 95) % 101 == 0:
            positions = Map2D.filled(width=101, height=103, element=0)
            for robot in robots:
                r = robot.r + steps * robot.v
                i = r[0] % positions.width
                j = r[1] % positions.height
                positions.update(i, j, lambda n: n + 1)
            print(steps)
            print(positions.format(formatter=lambda n: str(n) if n > 0 else " "))
            return
