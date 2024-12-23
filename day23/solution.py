import collections
import itertools


def parse_graph(inp: str) -> dict[str, set[str]]:
    g: dict[str, set[str]] = collections.defaultdict(set)
    for line in inp.splitlines():
        n1, n2 = line.split("-")
        g[n1].add(n2)
        g[n2].add(n1)
    return dict(g)


def part_1(inp: str, debug: bool):
    g = parse_graph(inp)
    triangles: set[tuple[str, ...]] = set()
    for n, connected in g.items():
        if not n.startswith("t"):
            continue
        conn_list = list(connected)
        for i in range(len(conn_list)):
            for j in range(i + 1, len(conn_list)):
                n1 = conn_list[i]
                n2 = conn_list[j]
                if n1 in g and n2 in g[n1]:
                    triangles.add(tuple(sorted([n, n1, n2])))
    print(len(triangles))


def part_2(inp: str, debug: bool):
    g = parse_graph(inp)

    cliques: list[set[str]] = []

    def bron_kerbosch(current_clique: set[str], pool: set[str], visited: set[str]) -> None:
        if not pool and not visited:
            cliques.append(current_clique)
        for v in pool:
            if v in visited:
                continue
            neighbors = g.get(v, set())
            bron_kerbosch(
                current_clique=current_clique.union({v}),
                pool=pool.intersection(neighbors),
                visited=visited.intersection(neighbors),
            )
            visited.add(v)

    bron_kerbosch(current_clique=set(), pool=set(g.keys()), visited=set())

    max_len = max(len(c) for c in cliques)
    max_clique = next(c for c in cliques if len(c) == max_len)
    print(",".join(sorted(max_clique)))
