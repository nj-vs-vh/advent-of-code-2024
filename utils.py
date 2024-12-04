from dataclasses import dataclass
from typing import Callable, Generic, TypeVar, cast
from collections.abc import Generator

T = TypeVar("T")


@dataclass
class Map2D(Generic[T]):
    content: list[list[T]]

    def __post_init__(self) -> None:
        self.height = len(self.content)
        self.width = len(self.content[0]) if self.content else 0

    def at(self, i: int, j: int) -> T | None:
        if 0 <= i < self.height and 0 <= j < self.width:
            return self.content[i][j]
        else:
            return None

    @classmethod
    def parse(cls, inp: str, char_parser: Callable[[str], T] | None = None) -> "Map2D":
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

    def iter_cells(self) -> Generator[tuple[int, int, T], None, None]:
        for i, row in enumerate(self.content):
            for j, cell in enumerate(row):
                yield i, j, cell
