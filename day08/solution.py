import collections
import itertools


def parse(inp: str) -> tuple[dict[str, list[complex]], int, int]:
    input_lines = inp.splitlines()
    h = len(input_lines)
    w = len(input_lines[0])

    named_antennas: dict[str, list[complex]] = collections.defaultdict(list)
    for a, line in enumerate(input_lines):
        for b, ch in enumerate(line):
            if ch != ".":
                named_antennas[ch].append(complex(b, a))
    return named_antennas, w, h


def part_1(inp: str, debug: bool):
    named_antennas, w, h = parse(inp)
    antinodes: set[complex] = set()
    for antennas in named_antennas.values():
        for a1, a2 in itertools.product(antennas, antennas):
            if a1 == a2:
                continue
            for first, second in ((a1, a2), (a2, a1)):
                antinode = first + (second - first) * 2
                if 0 <= antinode.real < w and 0 <= antinode.imag < h:
                    antinodes.add(antinode)
    print(len(antinodes))


def part_2(inp: str, debug: bool):
    named_antennas, w, h = parse(inp)
    antinodes: set[complex] = set()
    for antennas in named_antennas.values():
        for a1, a2 in itertools.product(antennas, antennas):
            if a1 == a2:
                continue
            delta = a2 - a1
            for harmonics_iter in (
                itertools.count(start=0, step=1),
                itertools.count(start=-1, step=-1),
            ):
                for harmonic in harmonics_iter:
                    antinode = a1 + delta * harmonic
                    if 0 <= antinode.real < w and 0 <= antinode.imag < h:
                        antinodes.add(antinode)
                    else:
                        break
    print(len(antinodes))
