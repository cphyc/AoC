from pathlib import Path

import numpy as np


def read_input():
    with open(Path(__file__).parent / "input_day6.txt") as f:
        return np.array([int(_) for _ in f.readline().split(",")])

    # return np.array([3,4,3,1,2])


def lanterfish_simulator(Ndays):
    ages = read_input()
    count_by_age = np.zeros(9, dtype=int)

    for i in range(9):
        count_by_age[i] = np.sum(ages == i)

    for i in range(Ndays):
        Nspawn = count_by_age[0]

        for j in range(1, 9):
            count_by_age[j - 1] = count_by_age[j]
        count_by_age[8] = Nspawn
        count_by_age[6] += Nspawn

    print("Part 1:", np.sum(count_by_age))


def solve_part_one():
    lanterfish_simulator(80)


def solve_part_two():
    lanterfish_simulator(256)


solve_part_one()
solve_part_two()
