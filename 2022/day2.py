import typing
from pathlib import Path

ROCK = 1
PAPER = 2
SCISSORS = 3


def read_input() -> typing.Generator[tuple[int, int], None, None]:
    with open(Path(__file__).parent / "input2") as f:
        lines = (_.strip() for _ in f.readlines())

    for line in lines:
        match line[0]:
            case "A":
                theirs = ROCK
            case "B":
                theirs = PAPER
            case "C":
                theirs = SCISSORS
        match line[2]:
            case "X":
                ours = ROCK
            case "Y":
                ours = PAPER
            case "Z":
                ours = SCISSORS
        yield theirs, ours


def part1():
    score = 0
    for theirs, ours in read_input():
        score += ours
        match (theirs, ours):
            # We win
            case (1, 2) | (2, 3) | (3, 1):
                score += 6
            case (a, b) if a == b:
                score += 3
            case _:
                score += 0
    print("Day 2, Part I:", score)


part1()
