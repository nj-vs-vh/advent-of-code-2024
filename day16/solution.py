import collections
import queue
from re import I
from time import sleep
from utils import IntVec2D, Map2D
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


@dataclass
class Node:
    distance: int
    state: State


def part_1(inp: str, debug: bool):
    map = Map2D.parse(inp)
    start_cell = map.first_where(lambda ch: ch == "S")
    assert start_cell != None

    pq = [Node(distance=0, state=State(start_cell, E))]
    visited: set[State] = set()
    while pq:
        current = pq.pop(0)
        visited.add(current.state)
        if map.at(*current.state.r) == "E":
            print(current.distance)
            return

        new_node_candidates: list[Node] = [
            Node(
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
            new_node_candidates.append(
                Node(distance=current.distance + 1, state=State(r=next_r, dir=current.state.dir))
            )

        for new_node in new_node_candidates:
            if new_node.state in visited:
                continue
            for node in pq:
                if node.state == new_node.state:
                    if node.distance > new_node.distance:
                        node.distance = new_node.distance
                    break
            else:
                pq.append(new_node)
        pq.sort(key=lambda n: n.distance)


def part_2(inp: str, debug: bool):
    map = Map2D.parse(inp)
    start = map.first_where(lambda ch: ch == "S")
    assert start != None
    end = map.first_where(lambda ch: ch == "E")
    assert end is not None

    pq = [Node(distance=0, state=State(start, E))]
    visited: set[State] = set()
    lead_to: dict[State, set[State]] = collections.defaultdict(set)
    while pq:
        current = pq.pop(0)
        visited.add(current.state)
        if map.at(*current.state.r) == "E":
            break

        new_node_candidates: list[Node] = [
            Node(
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
            new_node_candidates.append(
                Node(distance=current.distance + 1, state=State(r=next_r, dir=current.state.dir))
            )

        for new_node in new_node_candidates:
            if new_node.state in visited:
                continue
            for node in pq:
                if node.state == new_node.state:
                    if new_node.distance < node.distance:
                        node.distance = new_node.distance
                        lead_to[new_node.state] = {current.state}
                    elif new_node.distance == node.distance:
                        lead_to[new_node.state].add(current.state)
                    break
            else:
                lead_to[new_node.state] = {current.state}
                pq.append(new_node)
        pq.sort(key=lambda n: n.distance)

    # print(map.format(fmt))

    bt_tiles = set[IntVec2D]()
    bt_states: set[State] = {State(r=end, dir=d) for d in delta.keys()}
    while bt_states:
        bt_tiles.update(s.r for s in bt_states)
        new_bt_states = set()
        for s in bt_states:
            new_bt_states.update(lead_to.get(s, set()))
        bt_states = new_bt_states

    def fmt(ch: str, pos: tuple[int, int]) -> str:
        if pos in bt_tiles:
            return "O"
        if any(s.r == pos for s in visited):
            return "v"
        elif any(el.state.r == pos for el in pq):
            return "+"
        elif ch == ".":
            return " "
        else:
            return ch

    if debug:
        print(map.format(fmt))

    print(len(bt_tiles))
