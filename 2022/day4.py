from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Span:
    left: int
    right: int

    def __contains__(self, other: "Span") -> bool:
        return self.left <= other.left and self.right >= other.right


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


part1()
