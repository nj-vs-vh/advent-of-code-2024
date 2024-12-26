from functools import cache
import itertools
import re
from dataclasses import dataclass
from typing import Literal

import matplotlib.pyplot as plt
import networkx as nx  # type: ignore

OPERATION_RE = re.compile(r"^(\w+) (OR|AND|XOR) (\w+) -> (\w+)$")


@dataclass
class Operation:
    operand_1: str
    op: Literal["OR", "AND", "XOR"]
    operand_2: str
    output: str

    def __str__(self) -> str:
        return f"{self.operand_1} {self.op} {self.operand_2} => {self.output}"

    @classmethod
    def parse(cls, line: str) -> "Operation":
        m = OPERATION_RE.match(line)
        assert m is not None
        return Operation(
            operand_1=m.group(1),
            op=m.group(2),  # type: ignore
            operand_2=m.group(3),
            output=m.group(4),
        )


def parse(inp: str) -> tuple[dict[str, bool], dict[str, Operation]]:
    p1, p2 = inp.split("\n\n")
    init_values = {
        name: value == "1" for name, value in (line.split(": ") for line in p1.splitlines())
    }
    operations = [Operation.parse(line) for line in p2.splitlines()]
    return init_values, {o.output: o for o in operations}


def make_dependency_graph(operations: dict[str, Operation]) -> nx.DiGraph:
    G = nx.DiGraph()
    for output, operation in operations.items():
        G.add_edge(operation.operand_1, output, op=operation.op)
        G.add_edge(operation.operand_2, output, op=operation.op)
    return G


def calculate(graph: nx.DiGraph, values: dict[str, bool], assume_zeros: bool = False) -> list[bool]:
    for nodes in nx.topological_generations(graph):
        for out in nodes:
            if out in values:
                continue
            operands: list[str] = list(graph.predecessors(out))
            if len(operands) != 2:
                if assume_zeros:
                    continue
                else:
                    raise ValueError(
                        f"Corrupted graph or insufficient inputs: can't calculate {out}"
                    )
            in1, in2 = operands
            in1_value = values.get(in1, False)
            in2_value = values.get(in2, False)
            op = graph.get_edge_data(in1, out)["op"]
            match op:
                case "AND":
                    out_value = in1_value and in2_value
                case "OR":
                    out_value = in1_value or in2_value
                case "XOR":
                    out_value = in1_value != in2_value
                case _:
                    raise ValueError(f"Unexpected operation in edge {in1}->{out}: {op}")
            values[out] = out_value
    zs = sorted((k for k in values if k.startswith("z")), reverse=True)
    return [values[z] for z in zs]


def parse_bitlist(bitlist: list[bool]) -> int:
    result = "".join(["1" if b else "0" for b in bitlist])
    return int(result, base=2)


def part_1(inp: str, debug: bool):
    values, operations = parse(inp)
    g = make_dependency_graph(operations)
    result_bits = calculate(g, values)
    result = "".join(["1" if b else "0" for b in result_bits])
    print(result)
    print(int(result, base=2))


def varname(name: str, num: int) -> str:
    return f"{name}{num:0>2}"


def plot_topological(graph: nx.DiGraph, filename: str):
    for layer, nodes in enumerate(nx.topological_generations(graph)):
        for node in nodes:
            graph.nodes[node]["layer"] = layer
    op_colors = {
        "AND": "red",
        "XOR": "green",
        "OR": "blue",
    }

    pos = nx.multipartite_layout(graph, subset_key="layer")
    fig, ax = plt.subplots(figsize=(30, 30))
    nx.draw_networkx_nodes(graph, pos=pos, ax=ax, node_color="yellow")
    nx.draw_networkx_labels(graph, pos, font_size=11)
    nx.draw_networkx_edges(
        graph,
        pos,
        edge_color=[op_colors[edgedata["op"]] for _, _, edgedata in graph.edges(data=True)],
    )
    fig.savefig(fname=filename)


def make_adder_operations(n_bits: int) -> dict[str, Operation]:
    res: list[Operation] = []
    res.append(Operation(varname("x", 0), "XOR", varname("y", 0), varname("z", 0)))
    res.append(Operation(varname("x", 0), "AND", varname("y", 0), varname("_CARRY", 0)))
    for i in range(1, n_bits + 1):
        temp_0 = f"_TEMP_{i}_0"
        temp_1 = f"_TEMP_{i}_1"
        temp_2 = f"_TEMP_{i}_2"
        res.append(Operation(varname("x", i), "XOR", varname("y", i), temp_0))
        res.append(Operation(varname("x", i), "AND", varname("y", i), temp_1))
        res.append(Operation(varname("_CARRY", i - 1), "XOR", temp_0, varname("z", i)))
        res.append(Operation(varname("_CARRY", i - 1), "AND", temp_0, temp_2))
        res.append(
            Operation(
                temp_1,
                "OR",
                temp_2,
                output=varname("_CARRY", i) if i < n_bits else varname("z", i + 1),
            )
        )
    return {o.output: o for o in res}


def test_adder(ag: nx.DiGraph, n_bits: int) -> None:
    max_input = (2**n_bits) - 1
    for x in reversed(range(max_input)):
        for y in reversed(range(max_input)):
            values = {}
            x_bits = list(reversed(bin(x).removeprefix("0b")))
            for i_bit in range(n_bits):
                value = x_bits[i_bit] if i_bit < len(x_bits) else "0"
                values[varname("x", i_bit)] = value == "1"
            y_bits = list(reversed(bin(y).removeprefix("0b")))
            for i_bit in range(n_bits):
                value = y_bits[i_bit] if i_bit < len(y_bits) else "0"
                values[varname("y", i_bit)] = value == "1"
            z_actual = parse_bitlist(calculate(graph=ag, values=values, assume_zeros=True))
            z_expected = x + y
            if z_actual != z_expected:
                print(f"FAIL: {x} + {y} = {z_actual}")


def rename_to_match(g_source: nx.DiGraph, g_target: nx.DiGraph) -> None:
    renames: dict[str, str] = {}
    for layer_nodes in nx.topological_generations(g_target):
        for out in layer_nodes:
            operands_t: list[str] = list(g_target.predecessors(out))
            if len(operands_t) != 2:
                continue
            op1_t, op2_t = operands_t
            operation = g_target.get_edge_data(op1_t, out)
            op1_s = renames.get(op1_t, op1_t)
            op2_s = renames.get(op2_t, op2_t)
            if not (g_source.has_node(op1_s) and g_source.has_node(op2_s)):
                continue
            out_s = {
                o
                for o in set(g_source.successors(op1_s)).intersection(g_source.successors(op2_s))
                if g_source.get_edge_data(op1_s, o) == operation
            }
            if len(out_s) == 1:
                out_renamed = next(iter(out_s))
                if out != out_renamed:
                    renames[out] = out_renamed
    nx.relabel_nodes(g_target, renames, copy=False)


def part_2(inp: str, debug: bool):
    PLOT_FIRST_BITS = 43

    _, operations = parse(inp)

    operation_list = list(operations.values())
    SWAPS = [
        ("nnf", "z09"),
        ("nhs", "z20"),
        ("kqh", "ddn"),
        ("wrc", "z34"),
    ]
    print(",".join(sorted(itertools.chain.from_iterable(SWAPS))))
    for o1, o2 in SWAPS:
        for o in operation_list:
            if o.output == o1:
                o.output = o2
            elif o.output == o2:
                o.output = o1

    operations = {o.output: o for o in operation_list}
    g = make_dependency_graph(operations)

    test_bits = 3
    print(f"testing addition up to {test_bits} bits")
    test_adder(g, n_bits=test_bits)
    print("testing done")

    adder_ops = make_adder_operations(n_bits=PLOT_FIRST_BITS)
    adder_g = make_dependency_graph(adder_ops)
    rename_to_match(g, adder_g)
    # plot_topological(adder_g, "summer.png")

    not_relabeled = {node for node in adder_g.nodes if node.startswith("_")}
    if not_relabeled:
        print(f"some adder nodes are not relabeled: {not_relabeled}")

    @cache
    def trace_deps(o: str) -> set[str]:
        if o not in operations:
            return {o}
        operation = operations[o]
        return set().union(
            *(trace_deps(o_prev) for o_prev in (operation.operand_1, operation.operand_2))
        )

    def out_bit_subgraph(bit: int, inclusive: bool = False) -> nx.DiGraph:
        subgraph_nodes = set[str]()
        for b in range(bit + 1) if inclusive else [bit]:
            out_bit = varname("z", b)
            subgraph_nodes.add(out_bit)
            subgraph_nodes.update(nx.ancestors(g, out_bit))
        return g.subgraph(subgraph_nodes)

    # plot_topological(
    #     out_bit_subgraph(PLOT_FIRST_BITS, inclusive=True), filename="alleged_summer.png"
    # )

    def in_bit_subgraph(bit: int) -> nx.DiGraph:
        subgraph_nodes: set[str] = set()
        for letter in ("x", "y"):
            for b in range(bit + 1):
                inp = varname(letter, b)
                subgraph_nodes.add(inp)
                subgraph_nodes.update(nx.descendants(g, inp))
        return g.subgraph(subgraph_nodes)

    def test_bit_subgraph(bit: int) -> None:
        sg = out_bit_subgraph(bit)

        for carry in (True, False):
            inputs = {}
            for b in range(bit):
                inputs[varname("x", b)] = carry
                inputs[varname("y", b)] = carry
            for x, y in (
                (True, True),
                (True, False),
                (False, True),
                (False, False),
            ):
                z_expected = x ^ y
                if carry:
                    z_expected = not z_expected
                inputs[varname("x", bit)] = x
                inputs[varname("y", bit)] = y
                outputs = calculate(sg, values=inputs.copy())
                z_actual = outputs[0]
                if z_actual != z_expected:
                    print(f"{bit}: {carry=} {x=} {y=} expected z={z_expected} actual z={z_actual}")
