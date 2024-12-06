import copy
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

    def set(self, i: int, j: int, el: T) -> None:
        if 0 <= i < self.height and 0 <= j < self.width:
            self.content[i][j] = el

    def update(self, i: int, j: int, updater: Callable[[T], T]) -> None:
        if 0 <= i < self.height and 0 <= j < self.width:
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

    def iter_cells(self) -> Generator[tuple[int, int, T], None, None]:
        for i, row in enumerate(self.content):
            for j, cell in enumerate(row):
                yield i, j, cell

    def format(
        self,
        formatter: Callable[[T], str] = lambda t: str(t) if t is not None else " ",
        cell_width: int | None = None,
        rulers_each: int | None = None,
    ) -> str:
        # formatting
        str_map = [[formatter(cell) for cell in row] for row in self.content]
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
