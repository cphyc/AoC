from dataclasses import dataclass
from pathlib import Path

# from textwrap import dedent


class Op:
    pass


@dataclass
class Noop(Op):
    def __iter__(self):
        yield lambda x: x


@dataclass
class Addx(Op):
    x: int

    def __iter__(self):
        yield lambda x: x
        yield lambda x: x + self.x


def read_input():
    # raw_data = dedent(
    #     """\
    #     addx 15
    #     addx -11
    #     addx 6
    #     addx -3
    #     addx 5
    #     addx -1
    #     addx -8
    #     addx 13
    #     addx 4
    #     noop
    #     addx -1
    #     addx 5
    #     addx -1
    #     addx 5
    #     addx -1
    #     addx 5
    #     addx -1
    #     addx 5
    #     addx -1
    #     addx -35
    #     addx 1
    #     addx 24
    #     addx -19
    #     addx 1
    #     addx 16
    #     addx -11
    #     noop
    #     noop
    #     addx 21
    #     addx -15
    #     noop
    #     noop
    #     addx -3
    #     addx 9
    #     addx 1
    #     addx -3
    #     addx 8
    #     addx 1
    #     addx 5
    #     noop
    #     noop
    #     noop
    #     noop
    #     noop
    #     addx -36
    #     noop
    #     addx 1
    #     addx 7
    #     noop
    #     noop
    #     noop
    #     addx 2
    #     addx 6
    #     noop
    #     noop
    #     noop
    #     noop
    #     noop
    #     addx 1
    #     noop
    #     noop
    #     addx 7
    #     addx 1
    #     noop
    #     addx -13
    #     addx 13
    #     addx 7
    #     noop
    #     addx 1
    #     addx -33
    #     noop
    #     noop
    #     noop
    #     addx 2
    #     noop
    #     noop
    #     noop
    #     addx 8
    #     noop
    #     addx -1
    #     addx 2
    #     addx 1
    #     noop
    #     addx 17
    #     addx -9
    #     addx 1
    #     addx 1
    #     addx -3
    #     addx 11
    #     noop
    #     noop
    #     addx 1
    #     noop
    #     addx 1
    #     noop
    #     noop
    #     addx -13
    #     addx -19
    #     addx 1
    #     addx 3
    #     addx 26
    #     addx -30
    #     addx 12
    #     addx -1
    #     addx 3
    #     addx 1
    #     noop
    #     noop
    #     noop
    #     addx -9
    #     addx 18
    #     addx 1
    #     addx 2
    #     noop
    #     noop
    #     addx 9
    #     noop
    #     noop
    #     noop
    #     addx -1
    #     addx 2
    #     addx -37
    #     addx 1
    #     addx 3
    #     noop
    #     addx 15
    #     addx -21
    #     addx 22
    #     addx -6
    #     addx 1
    #     noop
    #     addx 2
    #     addx 1
    #     noop
    #     addx -10
    #     noop
    #     noop
    #     addx 20
    #     addx 1
    #     addx 2
    #     addx 2
    #     addx -6
    #     addx -11
    #     noop
    #     noop
    #     noop"""
    # )
    # if True:
    #     for line in raw_data.splitlines():
    with open(Path(__file__).parent / "input10") as f:
        while line := f.readline().strip():
            if line == "noop":
                yield Noop()
            elif line.startswith("addx"):
                yield Addx(int(line.split()[1]))


def part1():
    tick = 1
    x = 1
    strengths = []
    for op in read_input():
        for f in op:
            if (tick - 20) % 40 == 0:
                strengths.append(tick * x)
            x = f(x)
            tick += 1
    print("Sum of the signal strength: ", sum(strengths))


part1()
