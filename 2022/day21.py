from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable

from scipy.optimize import brentq

raw_input = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""

raw_input = (Path(__file__).parent / "input21").read_text()


class Operation(Enum):
    ADD = "+"
    MUL = "*"
    SUB = "-"
    DIV = "/"


@dataclass
class Monkey:
    name: str
    operation: int | tuple[str, Operation, str] | Callable

    @classmethod
    def from_line(cls, line: str) -> "Monkey":
        name, job = line.split(": ")
        match job.split():
            case [val]:
                return cls(name, int(val))
            case [left, op, right]:
                return cls(name, (left, Operation(op), right))
            case _:
                raise ValueError(f"Invalid job: {job}")

    @property
    def is_resolved(self) -> bool:
        return isinstance(self.operation, int) or callable(self.operation)


@dataclass
class MonkeyBand:
    monkeys: dict[str, Monkey]

    @classmethod
    def from_lines(cls, lines: list[str]) -> "MonkeyBand":
        return cls({monkey.name: monkey for monkey in map(Monkey.from_line, lines)})

    def find_number(self, key: str = "root") -> int:
        monkey = self.monkeys[key]

        if monkey.is_resolved:
            return monkey.operation  # type: ignore

        monkey1_key, op, monkey2_key = monkey.operation  # type: ignore

        monkey1 = self.find_number(monkey1_key)
        monkey2 = self.find_number(monkey2_key)

        if op == Operation.ADD:
            monkey.operation = monkey1 + monkey2
        elif op == Operation.MUL:
            monkey.operation = monkey1 * monkey2
        elif op == Operation.SUB:
            monkey.operation = monkey1 - monkey2
        elif op == Operation.DIV:
            monkey.operation = monkey1 // monkey2

        return monkey.operation  # type: ignore

    def find_number_abstract(self, key: str = "root") -> Callable:
        monkey = self.monkeys[key]

        if isinstance(monkey.operation, int):
            return lambda x: monkey.operation
        elif callable(monkey.operation):
            return monkey.operation

        monkey1_key, op, monkey2_key = monkey.operation  # type: ignore

        monkey1 = self.find_number_abstract(monkey1_key)
        monkey2 = self.find_number_abstract(monkey2_key)

        if op == Operation.ADD:
            monkey.operation = lambda x: monkey1(x) + monkey2(x)
        elif op == Operation.MUL:
            monkey.operation = lambda x: monkey1(x) * monkey2(x)
        elif op == Operation.SUB:
            monkey.operation = lambda x: monkey1(x) - monkey2(x)
        elif op == Operation.DIV:
            monkey.operation = lambda x: monkey1(x) // monkey2(x)
        else:
            raise ValueError(f"Invalid op")

        return monkey.operation


def part1():
    band = MonkeyBand.from_lines(raw_input.splitlines())
    print(f"Root has number {band.find_number()}.")


def part2():
    band = MonkeyBand.from_lines(raw_input.splitlines())
    band.monkeys["humn"].operation = lambda x: x
    left = band.find_number_abstract(band.monkeys["root"].operation[0])
    right = band.find_number_abstract(band.monkeys["root"].operation[2])

    # We know have two methods, left and right, find the root of their difference
    diff = lambda x: left(x) - right(x)
    xL = 3000000000000  # magic numbers: found by hand
    xR = 4000000000000  # magic numbers: found by hand
    xM = (xL + xR) // 2

    while xL + 1 != xR:
        d = diff(xM)
        if d > 0:
            xL = xM
        elif d < 0:
            xR = xM
        else:
            break

        xM = (xL + xR) // 2
    print(f"If I shout {xM}, then root receives twice {left(xM)}")


part1()
part2()
