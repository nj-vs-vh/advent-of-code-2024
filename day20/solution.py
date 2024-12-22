from utils import (
    DijkstraPriorityQueue,
    IntVec2D,
    Map2D,
    PathfindingNode,
    manhattan_neighborhood,
    manhattan_steps_cw,
)


def build_path_map(inp: str) -> Map2D[int | None]:
    map: Map2D[str] = Map2D.parse(inp)
    start = map.first_where(lambda ch: ch == "S")

    path_map: Map2D[int | None] = Map2D.filled_like(map, element=None)

    pq = DijkstraPriorityQueue(initial_state=start)
    while not pq.empty():
        node = pq.visit_next()
        path_map.set(*node.state, node.distance)
        for next_pos in manhattan_steps_cw(*node.state):
            if map.at(*next_pos) in {".", "E"}:
                pq.new_candidate(
                    PathfindingNode(distance=node.distance + 1, state=IntVec2D(*next_pos))
                )

    return path_map


def count_skips_above_100(path_map: Map2D[int | None], skip_len: int) -> int:
    skips: list[tuple[tuple[int, int], tuple[int, int], int]] = []
    for i, j, d_before in path_map.iter_cells():
        skip_start = (i, j)
        if d_before is None:
            continue
        for skip_end, delta in manhattan_neighborhood(r=skip_len, center=skip_start):
            d_after = path_map.at(*skip_end)
            if d_after is None or d_after < d_before:
                continue
            skip = (d_after - d_before) - delta
            if skip > 99:
                skips.append((skip_start, skip_end, skip))
    return len(skips)


def part_1(inp: str, debug: bool):
    path_map = build_path_map(inp)
    print(count_skips_above_100(path_map, skip_len=2))


def part_2(inp: str, debug: bool):
    path_map = build_path_map(inp)
    print(count_skips_above_100(path_map, skip_len=20))
