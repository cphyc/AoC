from pathlib import Path

import numpy as np


def read_input():
    with open(Path(__file__).parent / "input_day5.txt") as f:
        lines = f.readlines()

    # return np.array([
    #     [0,9,5,9],
    #     [8,0,0,8],
    #     [9,4,3,4],
    #     [2,2,2,1],
    #     [7,0,7,4],
    #     [6,4,2,0],
    #     [0,9,2,9],
    #     [3,4,1,4],
    #     [0,0,8,8],
    #     [5,5,8,2],
    # ])

    for line in lines:
        start, end = line.split("->")
        x1, y1 = (int(_) for _ in start.split(","))
        x2, y2 = (int(_) for _ in end.split(","))

        yield x1, y1, x2, y2


def solve_part_one():
    xmax, ymax = 0, 0
    for x1, y1, x2, y2 in read_input():
        xmax = max(x1, x2, xmax)
        ymax = max(y1, y2, ymax)

    grid = np.zeros((xmax + 1, ymax + 1), dtype=int)
    for x1, y1, x2, y2 in read_input():
        if not (x1 == x2 or y1 == y2):
            continue
        slx = slice(min(x1, x2), max(x1, x2) + 1)
        sly = slice(min(y1, y2), max(y1, y2) + 1)
        grid[slx, sly] += 1

    print("Part 1:", np.sum(grid > 1))
    return grid


grid = solve_part_one()
