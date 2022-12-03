import typing
from pathlib import Path

from more_itertools import chunked

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


def part2():
    priority = 0
    for sack1, sack2, sack3 in chunked(read_input(), 3):
        s1 = set(sack1[0]).union(sack1[1])
        s2 = set(sack2[0]).union(sack2[1])
        s3 = set(sack3[0]).union(sack3[1])

        # Find intersection of all three sets
        s = s1 & s2 & s3
        if len(s) != 1:
            raise Exception("Invalid input")
        priority += compute_priority(next(iter(s)))
    print("Day 3, Part II:", priority)


part1()
part2()
