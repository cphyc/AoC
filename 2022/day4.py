from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Span:
    left: int
    right: int

    def __contains__(self, other: "Span") -> bool:
        return self.left <= other.left and self.right >= other.right

    @staticmethod
    def overlap(first: "Span", second: "Span") -> bool:
        return bool(
            set(range(first.left, first.right + 1))
            & set(range(second.left, second.right + 1))
        )


def read_input() -> Generator[tuple[Span, Span], None, None]:
    with (Path(__file__).parent / "input4").open() as f:
        while line := f.readline().strip():
            left, right = (
                Span(*(int(_) for _ in chunk.split("-"))) for chunk in line.split(",")
            )
            yield left, right


def part1():
    Noverlap = 0
    for left, right in read_input():
        if right in left or left in right:
            Noverlap += 1
    print("Day 4, Part I:", Noverlap)


def part2():
    Noverlap = 0
    for left, right in read_input():
        if Span.overlap(left, right):
            Noverlap += 1
    print("Day 4, Part II:", Noverlap)


part1()
part2()
