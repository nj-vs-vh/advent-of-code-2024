import copy
from utils import Map2D


UP = 1
RIGHT = 2
DOWN = 4
LEFT = 8


DELTA = {
    UP: (-1, 0),
    RIGHT: (0, 1),
    DOWN: (1, 0),
    LEFT: (0, -1),
}


TURN_RIGHT = {
    UP: RIGHT,
    RIGHT: DOWN,
    DOWN: LEFT,
    LEFT: UP,
}


def parse(inp) -> tuple[Map2D[bool], tuple[int, int]]:
    obstacle_map = Map2D.parse(inp, char_parser=lambda s: s == "#")
    for i, line in enumerate(inp.splitlines()):
        for j, char in enumerate(line):
            if char == "^":
                return obstacle_map, (i, j)
    raise RuntimeError("Failed to parse direction")


def part_1(inp: str, debug: bool):
    direction = UP
    obstacle_map, pos = parse(inp)

    path = Map2D.filled(obstacle_map.width, obstacle_map.height, False)
    path.set(*pos, True)
    while True:
        delta = DELTA[direction]
        next_pos = (pos[0] + delta[0], pos[1] + delta[1])
        next_obstacle = obstacle_map.at(*next_pos)
        if next_obstacle is None:
            break
        elif next_obstacle is True:
            direction = TURN_RIGHT[direction]
        else:
            pos = next_pos
            path.set(*pos, True)

    print(sum(sum(line) for line in path.content))


def trace_path(
    obstacle_map: Map2D[bool],
    pos: tuple[int, int],
    direction: int,
    directions_been: Map2D[int] | None,
    recurse: bool,
) -> int:
    initial_pos = pos
    added_obstruction_positions: set[tuple[int, int]] = set()

    directions_been.update(*pos, lambda d: d | direction)

    cycles = 0
    while True:
        delta = DELTA[direction]
        next_pos = (pos[0] + delta[0], pos[1] + delta[1])
        next_obstacle = obstacle_map.at(*next_pos)
        if next_obstacle is None:
            if added_obstruction_positions:
                print(len(added_obstruction_positions))
            return cycles
        elif next_obstacle is True:
            direction = TURN_RIGHT[direction]
        else:
            obstacle_map.set(*next_pos, True)
            if (
                recurse
                and next_pos != initial_pos
                and next_pos not in added_obstruction_positions
                and directions_been.at(*next_pos) == 0
            ):
                # what if next_pos was an obstacle?
                cycles_added = trace_path(
                    obstacle_map,
                    pos,
                    direction=TURN_RIGHT[direction],
                    directions_been=copy.deepcopy(directions_been),
                    recurse=False,
                )
                if cycles_added:
                    cycles += cycles_added
                    added_obstruction_positions.add(next_pos)
            obstacle_map.set(*next_pos, False)

            pos = next_pos
        if directions_been.at(*pos) & direction:
            return 1
        directions_been.update(*pos, lambda d: d | direction)


def part_2(inp: str, debug: bool):
    obstacle_map, pos = parse(inp)
    print(
        trace_path(
            obstacle_map=obstacle_map,
            pos=pos,
            direction=UP,
            directions_been=Map2D.filled(obstacle_map.width, obstacle_map.height, 0),
            recurse=True,
        )
    )
