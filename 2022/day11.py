from collections.abc import Callable
from dataclasses import dataclass
from math import prod
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
"""Monkey 0:
    Starting items: 79, 98
    Operation: new = old * 19
    Test: divisible by 23
        If true: throw to monkey 2
        If false: throw to monkey 3

Monkey 1:
    Starting items: 54, 65, 75, 74
    Operation: new = old + 6
    Test: divisible by 19
        If true: throw to monkey 2
        If false: throw to monkey 0

Monkey 2:
    Starting items: 79, 60, 97
    Operation: new = old * old
    Test: divisible by 13
        If true: throw to monkey 1
        If false: throw to monkey 3

Monkey 3:
    Starting items: 74
    Operation: new = old + 3
    Test: divisible by 17
        If true: throw to monkey 0
        If false: throw to monkey 1
"""

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


part1()
