from dataclasses import dataclass
from enum import Enum
from operator import methodcaller
from pathlib import Path

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
    operation: int | tuple[str, Operation, str]

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
        return isinstance(self.operation, int)


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


band = MonkeyBand.from_lines(raw_input.splitlines())
print(f"Root has number {band.find_number()}.")
