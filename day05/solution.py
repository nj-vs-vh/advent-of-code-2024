from collections import defaultdict
import copy
import functools
import pprint


def parse(inp: str):
    rules, pages = inp.split("\n\n")

    rules_parsed: dict[str, set[str]] = defaultdict(set)
    for rule in rules.splitlines():
        a, b = rule.split("|")
        a = int(a)
        b = int(b)
        rules_parsed[a].add(b)

    return rules_parsed, [[int(ch) for ch in line.split(",")] for line in pages.splitlines()]


def get_key(rules: dict[str, set[str]]):
    def cmp(a: int, b: int) -> int:
        if b in rules.get(a, set()):
            return -1
        if a in rules.get(b, set()):
            return 1
        else:
            return 0

    return functools.cmp_to_key(cmp)


def part_1(inp: str, debug: bool):
    rules, pages = parse(inp)
    key = get_key(rules)
    res = 0
    for page in pages:
        sorted_page = sorted(page, key=key)
        if page == sorted_page:
            res += page[len(page) // 2]
    print(res)


def part_2(inp: str, debug: bool):
    rules, pages = parse(inp)
    key = get_key(rules)
    res = 0
    for page in pages:
        sorted_page = sorted(page, key=key)
        if page != sorted_page:
            res += sorted_page[len(page) // 2]
    print(res)
