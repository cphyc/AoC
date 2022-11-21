import numpy as np
from pathlib import Path

def read_puzzle_input():
    with open(Path(__file__).parent / "input_day3.txt") as f:
        lines = [line.strip() for line in f.readlines() if line]

    tmp = []
    for line in lines:
        val = np.asarray([
            1 if char == "1" else 0
            for char in line
        ])
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
    
solve_part_one()
    