import collections
import queue
from re import I
from time import sleep
from utils import PathfindingNode, DijkstraPriorityQueue, IntVec2D, Map2D
from dataclasses import dataclass, field


N = 0
E = 1
S = 2
W = 3
delta = {
    N: IntVec2D(-1, 0),
    E: IntVec2D(0, 1),
    S: IntVec2D(1, 0),
    W: IntVec2D(0, -1),
}


@dataclass(frozen=True)
class State:
    r: IntVec2D
    dir: int


def node_candidates(
    current: PathfindingNode[State],
    map: Map2D[str],
) -> list[PathfindingNode[State]]:
    res: list[PathfindingNode] = [
        PathfindingNode(
            distance=current.distance + 1000,
            state=State(
                r=current.state.r,
                dir=(current.state.dir + dir_delta) % 4,
            ),
        )
        for dir_delta in (-1, 1)
    ]
    next_r = current.state.r + delta[current.state.dir]
    if map.at(*next_r) in {".", "E"}:
        res.append(
            PathfindingNode(
                distance=current.distance + 1, state=State(r=next_r, dir=current.state.dir)
            )
        )
    return res


def part_1(inp: str, debug: bool):
    map = Map2D.parse(inp)
    start_cell = map.first_where(lambda ch: ch == "S")
    assert start_cell != None

    pq = DijkstraPriorityQueue(initial_state=State(start_cell, E))
    while not pq.empty():
        current = pq.visit_next()
        if map.at(*current.state.r) == "E":
            print(current.distance)
            return

        for cand in node_candidates(current, map):
            pq.new_candidate(cand)


def part_2(inp: str, debug: bool):
    map = Map2D.parse(inp)
    start = map.first_where(lambda ch: ch == "S")
    assert start != None
    end = map.first_where(lambda ch: ch == "E")
    assert end is not None

    pq = DijkstraPriorityQueue(initial_state=State(start, E), backtrack=True)
    while not pq.empty():
        current = pq.visit_next()
        if map.at(*current.state.r) == "E":
            break

        for cand in node_candidates(current, map):
            pq.new_candidate(cand)
    # print(map.format(fmt))

    bt_tiles = set[IntVec2D]()
    for bt_states in pq.backtracking_steps(*(State(r=end, dir=d) for d in delta.keys())):
        bt_tiles.update(s.r for s in bt_states)

    def fmt(ch: str, pos: tuple[int, int]) -> str:
        if pos in bt_tiles:
            return "O"
        if any(s.r == pos for s in pq._visited):
            return "v"
        elif any(el.state.r == pos for el in pq._queue):
            return "+"
        elif ch == ".":
            return " "
        else:
            return ch

    if debug:
        print(map.format(fmt))

    print(len(bt_tiles))
