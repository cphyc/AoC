from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt


@dataclass
class Pos:
    x: int
    y: int

    def distance(self, other: "Pos") -> int:
        "Return the Manhattan distance between two points." ""
        return max(abs(self.x - other.x), abs(self.y - other.y))

    def move_towards(self, other: "Pos"):
        if self.distance(other) <= 1:
            return

        if self.x == other.x and abs(self.y - other.y) > 1:
            self.y = other.y + (1 if self.y > other.y else -1)
        elif self.y == other.y and abs(self.x - other.x) > 1:
            self.x = other.x + (1 if self.x > other.x else -1)
        elif self.x != other.x and self.y != other.y:
            self.x += 1 if self.x < other.x else -1
            self.y += 1 if self.y < other.y else -1

    def __add__(self, other: "Pos") -> "Pos":
        return Pos(self.x + other.x, self.y + other.y)

    def __iadd__(self, other: "Pos"):
        self.x += other.x
        self.y += other.y
        return self

    def copy(self) -> "Pos":
        return Pos(self.x, self.y)


def read_input() -> Generator[Pos, None, None]:
    raw_data = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""
    with open(Path(__file__).parent / "input9") as f:
        while line := f.readline():
            direction, step_len_str = line.split()
            # print(f"== {line} ==")
            step_len = int(step_len_str)
            match direction:
                case "R":
                    yield from (Pos(1, 0) for _ in range(step_len))
                case "L":
                    yield from (Pos(-1, 0) for _ in range(step_len))
                case "U":
                    yield from (Pos(0, 1) for _ in range(step_len))
                case "D":
                    yield from (Pos(0, -1) for _ in range(step_len))


def draw_grid(head, tail):
    s = [". . . . . .".split() for _ in range(5)]
    s[0][0] = "s"
    s[tail.y][tail.x] = "T"
    s[head.y][head.x] = "H"
    print()
    print("\n".join("".join(_) for _ in s[::-1]))


def part1():
    head = Pos(0, 0)
    tail = Pos(0, 0)

    visited_locations = [(0, 0)]
    for step in read_input():
        head += step

        oldTail = tail.copy()
        tail.move_towards(head)

        # draw_grid(head, tail)
        visited_locations.append((tail.x, tail.y))

    print("Rope visited this number of cells: ", len(set(visited_locations)))
    # plt.plot(*zip(*visited_locations))
    # plt.show()


part1()
