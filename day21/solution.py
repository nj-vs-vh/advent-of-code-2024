from functools import cache
import itertools
from utils import IntVec2D


NUMPAD = "789456123 0A"
NUMPAD_FORBIDDEN = IntVec2D(3, 0)
ARROW_PAD = " ^A<v>"
ARROW_FORBIDDEN = IntVec2D(0, 0)


def exec(cmd: str, pad: str, init: str) -> str:
    i, j = coords(init, pad)
    res = ""
    for ch in cmd:
        match ch:
            case ">":
                j += 1
            case "<":
                j -= 1
            case "^":
                i -= 1
            case "v":
                i += 1
            case "A":
                res += pad[i * 3 + j]
    return res


def numeric_value(numpad_cmd: str) -> int:
    return int(numpad_cmd.removesuffix("A"))


def coords(ch: str, pad: str) -> IntVec2D:
    i = pad.index(ch)
    return IntVec2D(i // 3, i % 3)


def _move_straight(a: IntVec2D, b: IntVec2D) -> str:
    if a[0] == b[0]:
        return abs(a[1] - b[1]) * ("<" if a[1] > b[1] else ">")
    elif a[1] == b[1]:
        return abs(a[0] - b[0]) * ("^" if a[0] > b[0] else "v")
    else:
        raise ValueError()


def move_and_press_commands(start: str, target: str, arrow_pad: bool) -> list[str]:
    pad = ARROW_PAD if arrow_pad else NUMPAD
    avoid_cell = ARROW_FORBIDDEN if arrow_pad else NUMPAD_FORBIDDEN
    from_ = coords(start, pad)
    to = coords(target, pad)

    if from_[0] == to[0] or from_[1] == to[1]:
        return [_move_straight(from_, to) + "A"]

    res: list[str] = []
    for turn in (IntVec2D(from_[0], to[1]), IntVec2D(to[0], from_[1])):
        if turn != avoid_cell:
            res.append(_move_straight(from_, turn) + _move_straight(turn, to) + "A")
    return res


def best_cmd_options(target_options: list[str], arrow_pad: bool) -> list[str]:
    res: list[str] = []
    best_len: int | None = None
    for target in target_options:
        command_options = [
            move_and_press_commands(s, t, arrow_pad=arrow_pad)
            for s, t in itertools.pairwise(itertools.chain("A", target))
        ]
        opts = ["".join(subcmds) for subcmds in itertools.product(*command_options)]
        opts_best_len = min(len(cmd) for cmd in opts)
        opts = [c for c in opts if len(c) == opts_best_len]
        if best_len is None or opts_best_len < best_len:
            best_len = opts_best_len
            res = opts
        elif opts_best_len == best_len:
            res.extend(opts)
    return res


def part_1(inp: str, debug: bool):
    res = 0
    for cmd_0 in inp.splitlines():
        cmd_1_opts = best_cmd_options([cmd_0], arrow_pad=False)
        # print(cmd_1_opts)
        cmd_2_opts = best_cmd_options(cmd_1_opts, arrow_pad=True)
        # print(cmd_2_opts)
        cmd_3_opts = best_cmd_options(cmd_2_opts, arrow_pad=True)
        complexity = numeric_value(cmd_0) * len(cmd_3_opts[0])
        print(len(cmd_3_opts[0]), complexity)
        res += complexity

    print(res)


@cache
def best_move_and_press_len(start: str, end: str, depth: int, arrow_pad: bool) -> int:
    if start == end:
        return 1  # just press A again...

    costs: list[int] = []
    for cmd in move_and_press_commands(start, end, arrow_pad=arrow_pad):
        if depth == 1:
            return len(cmd)  # at depth 1 all move->press commands are the same length
        cost = 0
        for c1, c2 in itertools.pairwise(itertools.chain("A", cmd)):
            cost += best_move_and_press_len(c1, c2, depth=depth - 1, arrow_pad=True)
        costs.append(cost)
    return min(costs)


def part_2(inp: str, debug: bool):
    res = 0
    for cmd in inp.splitlines():
        total_len = 0
        for c1, c2 in itertools.pairwise(itertools.chain("A", cmd)):
            total_len += best_move_and_press_len(c1, c2, depth=26, arrow_pad=False)
        complexity = numeric_value(cmd) * total_len
        res += complexity

    print(res)
