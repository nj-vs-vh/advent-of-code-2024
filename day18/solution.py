from utils import Map2D


def parse(inp: str):
    size, seq = inp.split("\n\n")
    w, h = size.split(" ")
    return int(w), int(h), [tuple(map(int, l.split(","))) for l in seq.splitlines()]


def part_1(inp: str, debug: bool):
    w, h, byteseq = parse(inp)
    sentinel = w * h + 1
    map = Map2D.filled(w, h, element=sentinel)
    for t, coords in enumerate(byteseq):
        map.set(*coords, t)

    print(map.format(lambda t: str(t) if t != sentinel else ".", cell_width=4))


def part_2(inp: str, debug: bool):
    pass
