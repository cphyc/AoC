from dataclasses import dataclass
from pathlib import Path
from typing import Generator

import numpy as np

raw_input = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""
raw_input = (Path(__file__).parent / "input14").read_text()


@dataclass
class Line:
    x: list[int]
    y: list[int]

    @classmethod
    def from_line(cls, line: str) -> "Line":
        all_x, all_y = [], []
        for x, y in ((int(_) for _ in chunk.split(",")) for chunk in line.split("->")):
            all_x.append(x)
            all_y.append(y)
        return cls(all_x, all_y)

    def strokes(self) -> Generator[tuple[int, int], None, None]:
        for i in range(len(self.x) - 1):
            x0, x1 = self.x[i], self.x[i + 1]
            y0, y1 = self.y[i], self.y[i + 1]

            if x0 == x1:
                y = y0
                while y != y1:
                    yield x0, y
                    y += 1 if y0 < y1 else -1
                yield x0, y
            else:
                x = x0
                while x != x1:
                    yield x, y0
                    x += 1 if x0 < x1 else -1
                yield x, y0


@dataclass
class Wall:
    lines: list[Line]
    mask: np.ndarray
    ymax: int

    @classmethod
    def from_lines(cls, lines: list[Line]) -> "Wall":
        xmax = max(max(line.x) for line in lines)
        ymax = max(max(line.y) for line in lines)

        mask = np.zeros((ymax + 1, xmax + 1), dtype=int)

        for line in lines:
            for (x, y) in line.strokes():
                mask[y, x] = 1

        return cls(lines, mask, ymax)

    def draw(self):
        mask_str = np.where(self.mask == 0, ".", np.where(self.mask == 1, "#", "o"))
        print("\n".join("".join(_ for _ in line) for line in mask_str[:, 494:504]))

    def pour_sand(self):
        x, y = 500, 0

        while y < self.ymax:
            # Can go down
            if self.mask[y + 1, x] == 0:
                y += 1
                continue

            # Can go left
            if self.mask[y + 1, x - 1] == 0:
                y += 1
                x -= 1
                continue

            # Can go right
            if self.mask[y + 1, x + 1] == 0:
                y += 1
                x += 1
                continue

            # Cannot go down, left or right
            break

        if y == self.ymax:
            return 1
        self.mask[y, x] = 2
        return 0


def part1():
    lines = [Line.from_line(line) for line in raw_input.splitlines()]
    wall = Wall.from_lines(lines)
    # wall.draw()

    out = 0
    Niter = 0
    while True:
        out = wall.pour_sand()
        if out == 0:
            Niter += 1
        else:
            break
        # wall.draw()
        # print()

    print(f"After {Niter} iterations, sand flows to the abyss")


part1()
