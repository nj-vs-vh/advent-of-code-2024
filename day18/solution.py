import itertools
from sre_parse import State
from utils import DijkstraPriorityQueue, IntVec2D, Map2D, PathfindingNode


def parse(inp: str):
    size, seq = inp.split("\n\n")
    w, h, takefirst = size.split(" ")
    return int(w), int(h), int(takefirst), [tuple(map(int, l.split(","))) for l in seq.splitlines()]


STEPS = (
    IntVec2D(-1, 0),
    IntVec2D(1, 0),
    IntVec2D(0, -1),
    IntVec2D(0, 1),
)


def shortest_path(w: int, h: int, byteseq: list[tuple[int, int]]) -> int | None:
    traversable = Map2D.filled(w, h, element=True)
    for coords in byteseq:
        traversable.set(*coords, False)

    pq = DijkstraPriorityQueue(initial_state=IntVec2D(0, 0))
    while not pq.empty():
        current = pq.visit_next()
        if current.state == (w - 1, h - 1):
            return current.distance

        for delta in STEPS:
            new = current.state + delta
            if traversable.at(*new):
                pq.new_candidate(PathfindingNode(distance=current.distance + 1, state=new))

    return None


def part_1(inp: str, debug: bool):
    w, h, takefirst, byteseq = parse(inp)
    print(shortest_path(w, h, byteseq[:takefirst]))


def part_2(inp: str, debug: bool):
    w, h, _, byteseq = parse(inp)
    low = 1
    assert shortest_path(w, h, byteseq[:low]) is not None
    high = len(byteseq)
    assert shortest_path(w, h, byteseq[:high]) is None
    while low < high - 1:
        print(low, high)
        mid = int(0.5 * (low + high))
        if shortest_path(w, h, byteseq[:mid]) is None:
            high = mid
        else:
            low = mid
    print(byteseq[low])
