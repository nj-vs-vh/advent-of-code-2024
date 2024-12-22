import collections
import collections.abc
import copy
import inspect
import itertools
import math
from collections.abc import Generator
from dataclasses import dataclass
from typing import Callable, Generic, Iterable, TypeVar, cast, overload

T = TypeVar("T")
T2 = TypeVar("T2")


@dataclass
class Map2D(Generic[T]):
    content: list[list[T]]

    def __post_init__(self) -> None:
        self.height = len(self.content)
        self.width = len(self.content[0]) if self.content else 0

    def is_inside(self, i: int, j: int) -> bool:
        return 0 <= i < self.height and 0 <= j < self.width

    def at(self, i: int, j: int) -> T | None:
        if self.is_inside(i, j):
            return self.content[i][j]
        else:
            return None

    def set(self, i: int, j: int, el: T) -> None:
        if self.is_inside(i, j):
            self.content[i][j] = el

    def update(self, i: int, j: int, updater: Callable[[T], T]) -> None:
        if self.is_inside(i, j):
            self.content[i][j] = updater(self.content[i][j])

    @classmethod
    def parse[T](cls, inp: str, char_parser: Callable[[str], T] | None = None) -> "Map2D[T]":
        content = [
            [
                (
                    char_parser(char) if char_parser else cast(T, char)
                )  # NOTE: default to no validation here
                for char in line
            ]
            for line in inp.splitlines()
        ]
        assert len({len(row) for row in content}) == 1, "Non-rectangular map!"
        return Map2D(content)

    @classmethod
    def filled[T](cls, width: int, height: int, element: T) -> "Map2D[T]":
        return Map2D([[copy.deepcopy(element) for _ in range(width)] for _ in range(height)])

    @classmethod
    def filled_like[T](cls, other: "Map2D", element: T) -> "Map2D[T]":
        return cls.filled(width=other.width, height=other.height, element=element)

    def iter_cells(self) -> Generator[tuple[int, int, T], None, None]:
        for i, row in enumerate(self.content):
            for j, cell in enumerate(row):
                yield i, j, cell

    def format(
        self,
        formatter: Callable[[T], str] | Callable[[T, tuple[int, int]], str] = lambda t: (
            str(t) if t is not None else " "
        ),
        cell_width: int | None = None,
        rulers_each: int | None = None,
    ) -> str:

        def formatter_wrap(el: T, pos: tuple[int, int]) -> str:
            if len(inspect.signature(formatter).parameters) == 1:
                return formatter(el)  # type: ignore
            else:
                return formatter(el, pos)  # type: ignore

        # formatting
        str_map = [
            [formatter_wrap(cell, (i, j)) for j, cell in enumerate(row)]
            for i, row in enumerate(self.content)
        ]
        # aligning all cells
        target_len = cell_width or max(max(len(s) for s in row) for row in str_map)
        str_map = [[s.center(target_len, " ") for s in row] for row in str_map]
        # inserting rulers
        ruler_cols: set[int] = set()
        if rulers_each is not None:
            for i_ruler in range(1, 1 + self.width // rulers_each):
                for row in str_map:
                    idx = i_ruler - 1 + i_ruler * rulers_each
                    if idx < len(row):
                        ruler_cols.add(idx)
                        row.insert(idx, "┆")
        top_bound_chars = ["┌"]
        bot_bound_chars = ["└"]
        horiz_ruler_chars = ["├"]
        for i in range(len(str_map[0])):
            top_bound_chars.append("─" * target_len if i not in ruler_cols else "┬")
            bot_bound_chars.append("─" * target_len if i not in ruler_cols else "┴")
            horiz_ruler_chars.append("┄" * target_len if i not in ruler_cols else "┼")
        top_bound_chars.append("┐")
        bot_bound_chars.append("┘")
        horiz_ruler_chars.append("┤")
        lines: list[str] = ["".join(top_bound_chars)]
        for i_row, row in enumerate(str_map):
            lines.append("".join(["│"] + row + ["│"]))
            if i_row != len(str_map) - 1 and rulers_each and (i_row + 1) % rulers_each == 0:
                lines.append("".join(horiz_ruler_chars))
        lines.append("".join(bot_bound_chars))
        return "\n".join(lines)

    def transform[T2](self, transformer: Callable[[T], T2]) -> "Map2D[T2]":
        return Map2D(content=[[transformer(el) for el in row] for row in self.content])

    def first_where(self, predicate: Callable[[T], bool]) -> "IntVec2D":
        for i, j, el in self.iter_cells():
            if predicate(el):
                return IntVec2D(i, j)
        raise ValueError("Not found")


def manhattan_steps_cw(i: int, j: int) -> Generator[tuple[int, int], None, None]:
    for di, dj in (
        (-1, 0),
        (0, 1),
        (1, 0),
        (0, -1),
    ):
        yield i + di, j + dj


class IntVec2D(tuple[int, int]):
    """Copy of Vec2D from turtle module, modified to work with integers"""

    def __new__(cls, x: int, y: int):
        return tuple.__new__(cls, (x, y))

    def __add__(self, other: "IntVec2D") -> "IntVec2D":  # type: ignore
        return IntVec2D(self[0] + other[0], self[1] + other[1])

    @overload  # type: ignore
    def __mul__(self, other: "IntVec2D") -> int:
        pass

    @overload
    def __mul__(self, other: int) -> "IntVec2D":
        pass

    def __mul__(self, other: "IntVec2D | int"):
        if isinstance(other, IntVec2D):
            return self[0] * other[0] + self[1] * other[1]
        return IntVec2D(self[0] * other, self[1] * other)

    def __rmul__(self, other):
        if isinstance(other, int):
            return IntVec2D(self[0] * other, self[1] * other)
        return NotImplemented

    def __sub__(self, other: "IntVec2D") -> "IntVec2D":
        return IntVec2D(self[0] - other[0], self[1] - other[1])

    def __neg__(self) -> "IntVec2D":
        return IntVec2D(-self[0], -self[1])

    def __abs__(self) -> float:
        return math.hypot(*self)

    def rotate_90_ccw(self) -> "IntVec2D":
        return IntVec2D(-self[1], self[0])

    def rotate_ccw(self, angle: int) -> "IntVec2D":
        """Angle is in units of pi/2 = 90 degrees"""
        match angle:
            case 0:
                return self
            case 1:
                return self.rotate_90_ccw()
            case 2:
                return IntVec2D(-self[0], -self[1])
            case 3:
                return self.rotate_ccw(2).rotate_ccw(1)
            case other:
                return self.rotate_ccw(other % 4)

    def __getnewargs__(self):
        return (self[0], self[1])

    def __repr__(self) -> str:
        return f"({self[0]}, {self[1]})"


StateT = TypeVar("StateT", bound=collections.abc.Hashable)


@dataclass
class PathfindingNode(Generic[StateT]):
    distance: int
    state: StateT


class DijkstraPriorityQueue(Generic[StateT]):
    """Simple list-based priority queue"""

    def __init__(self, initial_state: StateT, backtrack: bool = False) -> None:
        self.queue: list[PathfindingNode[StateT]] = []
        self.queue.append(PathfindingNode(distance=0, state=initial_state))
        self.visited: set[StateT] = set()
        self._backtrack = backtrack
        self.lead_to: dict[StateT, set[StateT]] = dict()
        self.current = PathfindingNode(distance=0, state=initial_state)

    def empty(self) -> bool:
        return not self.queue

    def visit_next(self) -> PathfindingNode[StateT]:
        self.queue.sort(key=lambda dn: dn.distance)
        current = self.queue.pop(0)
        self.visited.add(current.state)
        self.current = current
        return current

    def new_candidate(self, candidate: PathfindingNode[StateT]) -> None:
        if candidate.state in self.visited:
            return
        for node in self.queue:
            if node.state == candidate.state:
                if candidate.distance < node.distance:
                    node.distance = candidate.distance
                    if self._backtrack:
                        self.lead_to[candidate.state] = {self.current.state}
                elif candidate.distance == node.distance:
                    if self._backtrack:
                        self.lead_to[candidate.state].add(self.current.state)
                break
        else:
            if self._backtrack:
                self.lead_to[candidate.state] = {self.current.state}
            self.queue.append(candidate)

    def backtracking_steps(self, *from_: StateT) -> Generator[set[StateT], None, None]:
        states: set[StateT] = set(from_)
        while states:
            yield states
            new_states = set()
            for s in states:
                new_states.update(self.lead_to.get(s, set()))
            states = new_states


def manhattan_neighborhood(
    r: int, center: tuple[int, int]
) -> Generator[tuple[IntVec2D, int], None, None]:
    for di in range(-r, r + 1):
        width = r - abs(di)
        for dj in range(-width, width + 1):
            yield IntVec2D(center[0] + di, center[1] + dj), abs(di) + abs(dj)


def sliding_window(iterable: Iterable[T], n: int) -> Generator[tuple[T, ...], None, None]:
    "Collect data into overlapping fixed-length chunks or blocks."
    # sliding_window('ABCDEFG', 4) → ABCD BCDE CDEF DEFG
    iterator = iter(iterable)
    window = collections.deque(itertools.islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)
