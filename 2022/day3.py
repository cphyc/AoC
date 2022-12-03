import typing
from pathlib import Path

# example = """vJrwpWtwJgWrhcsFMMfFFhFp
# jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
# PmmdzqPrVvPwwTWBwg
# wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
# ttgJtRGJQctTZtZT
# CrZsJsPPZsGzwwsLwLmpwMDw""".splitlines()):


def read_input() -> typing.Generator[tuple[str, str], None, None]:
    with open(Path(__file__).parent / "input3") as f:
        while line := f.readline().strip():
            N = len(line) // 2
            yield line[:N], line[N:]


def compute_priority(c: str) -> int:
    if "A" <= c <= "Z":
        return ord(c) - ord("A") + 27
    elif "a" <= c <= "z":
        return ord(c) - ord("a") + 1
    else:
        raise Exception("Invalid character")


def part1():
    priority = 0
    # Iterate over rucksack compartments
    for comp1, comp2 in read_input():
        set_comp1 = set(comp1)
        set_comp2 = set(comp2)

        # Check if there is a common element
        set_common = set_comp1 & set_comp2
        priority += sum(compute_priority(c) for c in set_common)

    print("Day 3, Part I:", priority)


part1()
