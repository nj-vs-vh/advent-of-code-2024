from typing import Generator
from utils import Map2D, manhattan_steps_cw


def part_1(inp: str, debug: bool):
    plots = Map2D.parse(inp)
    fenced = Map2D.filled_like(plots, False)
    price = 0
    for i, j, plot in plots.iter_cells():
        if fenced.at(i, j):
            continue

        curr, nxt = {(i, j)}, set()
        area = 0
        perimeter = 0
        while curr:
            nxt.clear()
            for i, j in curr:
                fenced.set(i, j, True)
                area += 1
                for inext, jnext in manhattan_steps_cw(i, j):
                    if plots.at(inext, jnext) != plot:
                        perimeter += 1
                    elif not fenced.at(inext, jnext):
                        nxt.add((inext, jnext))
            curr, nxt = nxt, curr

        price += area * perimeter

    print(price)


def corner_neighbors(i: int, j: int) -> Generator[tuple[int, int], None, None]:
    for deltas in (
        ((-1, 0), (-1, 1), (0, 1)),
        ((0, 1), (1, 1), (1, 0)),
        ((1, 0), (1, -1), (0, -1)),
        ((0, -1), (-1, -1), (-1, 0)),
    ):
        yield [(i + di, j + dj) for di, dj in deltas]


def part_2(inp: str, debug: bool):
    plots = Map2D.parse(inp)
    fenced = Map2D.filled_like(plots, False)
    price = 0
    for i, j, plot in plots.iter_cells():
        if fenced.at(i, j):
            continue

        curr, nxt = {(i, j)}, set()
        area = 0
        corners = 0
        while curr:
            nxt.clear()
            for i, j in curr:
                fenced.set(i, j, True)
                area += 1
                for n1, corner, n2 in corner_neighbors(i, j):
                    if (plots.at(*n1) != plot and plots.at(*n2) != plot) or (  # convex corner
                        plots.at(*n1) == plot
                        and plots.at(*n2) == plot
                        and plots.at(*corner) != plot  # concave corner
                    ):
                        corners += 1
                        corner
                    if plots.at(*n1) == plot and not fenced.at(*n1):
                        nxt.add(n1)
            curr, nxt = nxt, curr

        price += area * corners

    print(price)
