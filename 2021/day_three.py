from pathlib import Path

import numpy as np


def read_puzzle_input():
    with open(Path(__file__).parent / "input_day3.txt") as f:
        lines = [line.strip() for line in f.readlines() if line]

    tmp = []
    for line in lines:
        val = np.asarray([1 if char == "1" else 0 for char in line])
        tmp.append(val)
    return np.asarray(tmp)


def solve_part_one():
    puzzle = read_puzzle_input()
    N, Ncol = puzzle.shape

    gamma, epsilon = 0b0, 0b0
    for col in range(Ncol):
        ones = np.sum(puzzle[:, col])
        gamma <<= 1
        epsilon <<= 1
        if ones > N / 2:
            gamma |= 0b1
        else:
            epsilon |= 0b1

    print("Part 1: ", gamma * epsilon)


def sum_bits(bitarray) -> int:
    v = 0
    for b in bitarray:
        v = (v << 1) | b
    return v


def solve_part_two():
    puzzle = read_puzzle_input()
    N, Ncol = puzzle.shape

    candidates = puzzle.copy()
    for col in range(Ncol):
        ones = np.sum(candidates[:, col])
        if ones >= (len(candidates) / 2):
            mask = candidates[:, col] == 1
        else:
            mask = candidates[:, col] == 0
        candidates = candidates[mask]

        if len(candidates) == 1:
            break

    oxygen_rating = sum_bits(candidates[0])

    candidates = puzzle.copy()
    for col in range(Ncol):
        ones = np.sum(candidates[:, col])
        if ones >= (len(candidates) / 2):
            mask = candidates[:, col] == 0
        else:
            mask = candidates[:, col] == 1
        candidates = candidates[mask]

        if len(candidates) == 1:
            break

    CO2_scrubber = sum_bits(candidates[0])

    print(oxygen_rating, CO2_scrubber)
    print("Part 2: ", oxygen_rating * CO2_scrubber)


solve_part_one()
solve_part_two()
