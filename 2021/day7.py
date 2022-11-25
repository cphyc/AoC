from pathlib import Path

import numpy as np


def load_input():
    # x0 = np.array([16,1,2,0,4,2,7,1,2,14])
    x0 = np.loadtxt(Path(__file__).parent / "input_day7.txt", dtype=int, delimiter=",")
    return x0


def solve_part_one():
    x0 = load_input()
    cost = {}
    for x in range(x0.min(), x0.max() + 1):
        cost[x] = np.sum(np.abs(x0 - x))

    keys = np.array(list(cost.keys()))
    costs = np.array(list(cost.values()))

    imin = np.argmin(costs)
    print(f"Part 1: position={keys[imin]} cost={costs[imin]}")


solve_part_one()
