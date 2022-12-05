import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

# Regular expression that matches move X from Y to Z, with X, Y, Z integers
MOVE_CMD = re.compile(r"move (\d+) from (\d+) to (\d+)")


@dataclass
class Stack:
    cranes: list[str]

    @staticmethod
    def from_iterable(cranes_iter: Iterable[str], *, reverse: bool = False) -> "Stack":
        return Stack(
            [
                crane
                for crane in (reversed(cranes_iter) if reverse else cranes_iter)
                if crane.strip()
            ]
        )

    def move_cranes(self, N: int, dest: "Stack", *, retain_order: bool = False):
        # Split cranes into two groups
        keep, move = self.cranes[:-N], self.cranes[-N:]

        self.cranes = keep

        if retain_order:
            dest.cranes.extend(move)
        else:
            dest.cranes.extend(reversed(move))


@dataclass
class Instruction:
    N: int
    ifrom: int
    ito: int

    @staticmethod
    def from_line(line: str) -> "Instruction":
        N, ifrom, ito = (int(_) for _ in MOVE_CMD.match(line).groups())
        ifrom -= 1
        ito -= 1
        return Instruction(N, ifrom, ito)


def read_input() -> tuple[list[Stack], list[Instruction]]:
    with (Path(__file__).parent / "input5").open() as f:
        lines = iter(f.readlines())

    # Read stacks
    stack_lines = []
    for line in lines:
        if not line.strip():
            break
        stack_lines.append(line)

    stack_lines.pop(-1)

    # Parse the stack definitions
    stacks = [
        Stack.from_iterable(cranes, reverse=True)
        for cranes in zip(*(list(sl[1::4]) for sl in stack_lines))
    ]

    # Restart iteration until eof
    instructions = [Instruction.from_line(line) for line in lines]

    return stacks, instructions


def part1():
    stacks, instructions = read_input()

    for instruction in instructions:
        stacks[instruction.ifrom].move_cranes(
            instruction.N, stacks[instruction.ito], retain_order=False
        )
    print("Day 5, Part I:", "".join(stack.cranes[-1] for stack in stacks))


def part2():
    stacks, instructions = read_input()

    for instruction in instructions:
        stacks[instruction.ifrom].move_cranes(
            instruction.N, stacks[instruction.ito], retain_order=True
        )
    print("Day 5, Part II:", "".join(stack.cranes[-1] for stack in stacks))


part1()
part2()
