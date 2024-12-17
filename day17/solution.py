import copy
from dataclasses import dataclass
import itertools
import math


@dataclass
class State:
    ra: int
    rb: int
    rc: int
    program: list[int]
    ptr: int
    outbuf: list[int]

    @classmethod
    def parse_init(cls, inp: str) -> "State":
        la, lb, lc, _, lprog = inp.splitlines()
        return State(
            ra=int(la.split(": ")[1]),
            rb=int(lb.split(": ")[1]),
            rc=int(lc.split(": ")[1]),
            program=list(map(int, lprog.split(": ")[1].split(","))),
            ptr=0,
            outbuf=[],
        )

    def format(self) -> str:
        instr_names = ["adv", "bxl", "bst", "jnz", "bxc", "out", "bdv", "cdv"]
        is_op_literal = [False, True, False, True, False, False, False, False]
        combo_op_names = ["0", "1", "2", "3", "ra", "rb", "rc", "INVALID"]
        program_lines = [
            f"{'-> ' if idx * 2 == self.ptr else '   '}{instr_names[instr]} {op if is_op_literal[instr] else combo_op_names[op]}"
            for idx, (instr, op) in enumerate(itertools.batched(self.program, n=2))
        ]
        return (
            f"\nout: {','.join(str(o) for o in self.outbuf)}\nra: {self.ra} rb: {self.rb} rc: {self.rc}\n"
            + "\n".join(program_lines)
        )

    def combo_operand(self, op: int) -> int:
        match op:
            case 0 | 1 | 2 | 3:
                return op
            case 4:
                return self.ra
            case 5:
                return self.rb
            case 6:
                return self.rc
            case _:
                raise ValueError("Invalid combo operand")

    def exec(self) -> bool:
        instr = self.program[self.ptr]
        operand = self.program[self.ptr + 1]
        match instr:
            case 0:  # adv
                self.ra = int(self.ra / (2 ** self.combo_operand(operand)))
            case 1:  # bxl
                self.rb = self.rb ^ operand
            case 2:  # bst
                self.rb = self.combo_operand(operand) % 8
            case 3:  # jnz
                if self.ra != 0:
                    self.ptr = operand
                    return True
            case 4:  # bxc
                self.rb = self.rb ^ self.rc
            case 5:  # out
                self.outbuf.append(self.combo_operand(operand) % 8)
            case 6:  # bdv
                self.rb = int(self.ra / (2 ** self.combo_operand(operand)))
            case 7:  # cdv
                self.rc = int(self.ra / (2 ** self.combo_operand(operand)))
            case _:
                raise ValueError(f"Unexpeted instruction {instr}")

        self.ptr += 2
        return self.ptr < len(self.program)

    def exec_until_output(self) -> bool:
        current_outbuf_len = len(self.outbuf)
        while True:
            runs = self.exec()
            if not runs or len(self.outbuf) != current_outbuf_len:
                return runs


def part_1(inp: str, debug: bool):
    state = State.parse_init(inp)
    py_impl(a_init=state.ra)
    while state.exec():
        if debug:
            print(state.format())
    print(state.format())


def py_impl_step(a: int) -> tuple[int, int]:
    triplet = a % 8
    out = triplet ^ 5 ^ 6 ^ (a // (2 ** (triplet ^ 5))) % 8
    a = a >> 3
    return out, a


def py_impl(a_init: int) -> None:
    a = a_init
    while a:
        out, a = py_impl_step(a)
        print(out, end=",")
    print()


def fmt(a: int, target_len: int | None = None) -> str:
    res = f"{a:b}"
    triplets_len = int(math.ceil(len(res) / 3) * 3)
    res = res.rjust(triplets_len, "0")
    if target_len is not None:
        res = res.ljust(target_len, " ")
    return " ".join("".join(ch for ch in batch) for batch in itertools.batched(res, n=3))


def get_a_0(a_i: int, outputs: list[int]) -> int | None:
    if not outputs:
        return a_i
    last_output = outputs[-1]
    for triplet in range(8):
        a_i_prev = (a_i << 3) + triplet
        if a_i_prev == 0:
            continue
        would_be_out, a_i_rec = py_impl_step(a_i_prev)
        assert a_i == a_i_rec
        if would_be_out == last_output:
            res = get_a_0(a_i=a_i_prev, outputs=outputs[:-1])
            if res is not None:
                return res
    else:
        return None


def part_2(inp: str, debug: bool):
    init_state = State.parse_init(inp)
    print(get_a_0(a_i=0, outputs=init_state.program))
