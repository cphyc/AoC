from collections.abc import Callable
from dataclasses import dataclass
from math import lcm, prod
from pathlib import Path
from typing import Literal

import pyparsing as pp


def doOperation(old: int, tokens: tuple[Literal["*", "+"], str]) -> int:
    op = tokens[0]
    if tokens[1] == "old":
        value = old
    else:
        value = int(tokens[1])

    if op == "*":
        return old * value
    elif op == "+":
        return old + value


@dataclass
class Monkey:
    id: int
    worry_levels: list[int]
    update_worry: Callable[[int], int]
    test: Callable[[int], bool]
    target_if_true: int
    target_if_false: int
    Ninspected: int = 0
    worry_divider: int = 3
    worry_remainder: int = 0

    @classmethod
    def from_tokens(cls, tokens):
        return cls(
            id=tokens[0],
            worry_levels=list(tokens[1][0]),
            update_worry=tokens[1][1],
            test=tokens[1][2],
            target_if_true=tokens[1][3][0],
            target_if_false=tokens[1][3][1],
        )

    def throw_item(self, worry: int, monkeys: list["Monkey"]):
        self.Ninspected += 1
        newWorry = self.update_worry(worry) // self.worry_divider
        if self.worry_remainder:
            newWorry %= self.worry_remainder

        if self.test(newWorry):
            itarget = self.target_if_true
        else:
            itarget = self.target_if_false

        # print(f"{self.id} throws item with worriness {newWorry} to {itarget}")

        monkeys[itarget].worry_levels.append(newWorry)


pp.ParserElement.set_default_whitespace_chars(" \t")
eol = pp.LineEnd()
StartingItems = pp.Group(
    (
        pp.Literal("Starting items:")
        + pp.delimitedList(pp.Word(pp.nums), delim=",")
        + eol
    ).set_parse_action(lambda tokens: [int(i) for i in tokens[1:-1]])
)

Operation = (
    pp.Literal("Operation: new = old")
    + (
        (
            pp.one_of(["*", "+"]) + (pp.Word(pp.nums) | pp.Literal("old"))
        ).set_parse_action(lambda tokens: (lambda old: doOperation(old, tokens)))
    )
    + eol
).set_parse_action(lambda tokens: tokens[1])
Test = (pp.Literal("Test: divisible by") + pp.Word(pp.nums) + eol).set_parse_action(
    lambda tokens: lambda x: x % int(tokens[1]) == 0
)
ConditionTrue = (
    pp.Literal("If true: throw to monkey") + pp.Word(pp.nums) + eol
).set_parse_action(lambda tokens: int(tokens[1]))
ConditionFalse = (
    pp.Literal("If false: throw to monkey") + pp.Word(pp.nums) + eol
).set_parse_action(lambda tokens: int(tokens[1]))
MonkeyDescription = pp.IndentedBlock(
    StartingItems
    + Operation
    + Test
    + pp.IndentedBlock(
        ConditionTrue + ConditionFalse,
    )
)
MonkeyName = (pp.Literal("Monkey") + pp.Word(pp.nums) + ":" + eol).set_parse_action(
    lambda tokens: int(tokens[1])
)
MonkeyDef = (MonkeyName + MonkeyDescription).set_parse_action(
    lambda tokens: Monkey.from_tokens(tokens)
)

MonkeyGrammar = pp.delimited_list(MonkeyDef, delim="\n")


raw_input = (Path(__file__).parent / "input11").read_text()

monkeys: list[Monkey] = list(MonkeyGrammar.parseString(raw_input))


def part1():
    for round in range(20):
        for monkey in monkeys:
            while monkey.worry_levels:
                itemWorry = monkey.worry_levels.pop(0)
                monkey.throw_item(itemWorry, monkeys)
        print(f"Round {round+1}")
        for monkey in monkeys:
            print(
                f"Monkey {monkey.id}: {', '.join(str(_) for _ in monkey.worry_levels)}"
            )
        print()

    two_most_active_monkeys = sorted(
        monkeys, key=lambda monkey: monkey.Ninspected, reverse=True
    )[:2]
    print(
        "Monkey business:",
        prod(monkey.Ninspected for monkey in two_most_active_monkeys),
    )


def part2():
    divisions = set()
    for monkey in monkeys:
        i = 1
        while not monkey.test(i):
            i += 1
        divisions.add(i)
    least_common_multiple = lcm(*divisions)

    for monkey in monkeys:
        monkey.worry_divider = 1
        monkey.worry_remainder = least_common_multiple

    for round in range(10_000):
        for monkey in monkeys:
            while monkey.worry_levels:
                itemWorry = monkey.worry_levels.pop(0)
                monkey.throw_item(itemWorry, monkeys)

        if round + 1 in (
            1,
            20,
            1000,
            2000,
            3000,
            4000,
            5000,
            6000,
            7000,
            8000,
            9000,
            10000,
        ):
            print(f"Round {round+1}")
            for monkey in monkeys:
                print(f"Monkey {monkey.id} insected items {monkey.Ninspected} times")
            print()

    two_most_active_monkeys = sorted(
        monkeys, key=lambda monkey: monkey.Ninspected, reverse=True
    )[:2]
    print(
        "Monkey business:",
        prod(monkey.Ninspected for monkey in two_most_active_monkeys),
    )


# part1()
part2()
