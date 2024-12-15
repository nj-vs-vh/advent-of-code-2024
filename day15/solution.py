import itertools
from typing import Literal
from utils import IntVec2D, Map2D


DIRECTIONS = {
    "^": IntVec2D(-1, 0),
    ">": IntVec2D(0, 1),
    "v": IntVec2D(1, 0),
    "<": IntVec2D(0, -1),
}


def parse(inp: str, pt2: bool) -> tuple[Map2D[str], list[IntVec2D]]:
    map_str, instructions_str = inp.split("\n\n")
    if pt2:
        map_str = (
            map_str.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
        )
    return (
        Map2D.parse(map_str, char_parser=lambda ch: ch if ch != "." else " "),
        [DIRECTIONS[ch] for ch in instructions_str if not ch.isspace()],
    )


def part_1(inp: str, debug: bool):
    map, instructions = parse(inp, pt2=False)
    robot = map.first_where(lambda ch: ch == "@")
    assert robot is not None
    ri, rj = robot
    for di, dj in instructions:
        moved_cells: list[tuple[int, int]] = [(ri, rj)]
        for length in itertools.count(start=1):
            ci = ri + length * di
            cj = rj + length * dj
            if map.at(ci, cj) == "#":
                moved_cells.clear()
                break
            elif map.at(ci, cj) == " ":
                break
            elif map.at(ci, cj) == "O":
                moved_cells.append((ci, cj))
            else:
                raise RuntimeError(map.at(ci, cj))

        if not moved_cells:
            continue

        moved_cell_contents = [map.at(*m) for m in moved_cells]
        for m in moved_cells:
            map.set(*m, " ")
        for (mi, mj), content in zip(moved_cells, moved_cell_contents):
            map.set(mi + di, mj + dj, content)  # type: ignore
        ri += di
        rj += dj

        if debug:
            print(map.format())
            input()

    res = 0
    for i, j, cell in map.iter_cells():
        if cell == "O":
            res += 100 * i + j
    print(res)


def part_2(inp: str, debug: bool):
    map, instructions = parse(inp, pt2=True)
    robot = map.first_where(lambda ch: ch == "@")
    assert robot is not None

    def get_moved_cells(
        map: Map2D[str],
        dir: tuple[int, int],
        robot: tuple[int, int],
    ) -> list[tuple[int, int]]:
        res: list[tuple[int, int]] = [robot]
        front: set[tuple[int, int]] = {robot}
        while front:
            next_front: set[tuple[int, int]] = set()
            for fi, fj in front:
                nfi = fi + dir[0]
                nfj = fj + dir[1]
                match map.at(nfi, nfj):
                    case "#":
                        return []
                    case " ":
                        pass
                    case "[":
                        res.append((nfi, nfj))
                        res.append((nfi, nfj + 1))
                        if dir[1] != 1:
                            next_front.add((nfi, nfj))
                        next_front.add((nfi, nfj + 1))
                    case "]":
                        res.append((nfi, nfj))
                        res.append((nfi, nfj - 1))
                        if dir[1] != -1:
                            next_front.add((nfi, nfj))
                        next_front.add((nfi, nfj - 1))
                    case _:
                        raise RuntimeError(f"Unexpected char: {map.at(nfi, nfj)}")
            front = next_front
        return res

    for dir in instructions:
        moved_cells = get_moved_cells(map, dir, robot)
        if not moved_cells:
            continue

        moved_cell_contents = [map.at(*m) for m in moved_cells]
        for m in moved_cells:
            map.set(*m, " ")
        for (mi, mj), content in zip(moved_cells, moved_cell_contents):
            map.set(mi + dir[0], mj + dir[1], content)  # type: ignore
        robot = robot + dir

        if debug:
            print(map.format())
            input()

    res = 0
    for i, j, cell in map.iter_cells():
        if cell == "[":
            res += 100 * i + j
    print(res)
