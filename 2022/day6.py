from collections import Counter
from pathlib import Path

from more_itertools import windowed


def read_input() -> str:
    with open(Path(__file__).parent / "input6") as f:
        return f.readline().strip()


def part1():
    buffer = read_input()
    for i, subset in enumerate(windowed(buffer, 4)):
        if Counter(subset).most_common(1)[0][1] == 1:
            break
    print("Day 6, part I:", i + 4)


def part2():
    buffer = read_input()
    for i, subset in enumerate(windowed(buffer, 14)):
        if Counter(subset).most_common(1)[0][1] == 1:
            break
    print("Day 6, part II:", i + 14)


part1()
part2()
