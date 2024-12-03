
import re


mul_regex = re.compile(r"mul\((\d+),(\d+)\)")

def part_1(inp: str, debug: bool):
    sum = 0
    for mul_match in mul_regex.finditer(inp):
        sum += int(mul_match.group(1)) * int(mul_match.group(2))
    print(sum)


instruction_regex = re.compile(r"(mul\((\d+),(\d+)\)|do\(\)|don\'t\(\))")


def part_2(inp: str, debug: bool):
    sum = 0
    is_enabled = True
    for instruction_match in instruction_regex.finditer(inp):
        instruction = instruction_match.group(1)
        match instruction:
            case "do()":
                is_enabled = True
            case "don't()":
                is_enabled = False
            case _:
                if is_enabled:
                    sum += int(instruction_match.group(2)) * int(instruction_match.group(3))
    print(sum)
