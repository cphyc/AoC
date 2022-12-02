import typing
from pathlib import Path


def read_input() -> typing.Generator[tuple[str, str], None, None]:
    with open(Path(__file__).parent / "input2") as f:
        while line := f.readline():
            yield line.strip().split()


def part1():
    score = 0
    for theirs, ours in read_input():
        score += dict(X=1, Y=2, Z=3)[ours]
        match (theirs, ours):
            case ("A", "Y") | ("B", "Z") | ("C", "X"):
                score += 6
            case ("A", "X") | ("B", "Y") | ("C", "Z"):
                score += 3
            case _:
                score += 0
    print("Day 2, Part I:", score)


def part2():
    score = 0
    lose_map = dict(A="Z", B="X", C="Y")
    win_map = dict(A="Y", B="Z", C="X")
    tie_map = dict(A="X", B="Y", C="Z")
    score_map = dict(X=1, Y=2, Z=3)
    for theirs, ours in read_input():
        if ours == "X":  # we need to lose
            score += 0
            will_play = lose_map[theirs]
        elif ours == "Y":  # we need to tie
            score += 3
            will_play = tie_map[theirs]
        elif ours == "Z":  # we need to win
            score += 6
            will_play = win_map[theirs]

        score += score_map[will_play]

    print("Day 2, Part II:", score)


part1()
part2()
