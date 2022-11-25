from pathlib import Path

import numpy as np


def read_input():
    with open(Path(__file__).parent / "input_day4.txt") as f:
        lines = f.readlines()

    bingo_input = np.array([int(_) for _ in lines[0].split(",")])

    grids = []
    acc = []
    lines.pop(0)
    while lines:
        line = lines.pop(0).strip()
        if not line:
            continue
        acc.append([int(_) for _ in line.split()])
        if len(acc) == 5:
            grids.append(np.array(acc))
            acc = []

    return bingo_input, grids


def solve_part_one():
    bingo_input, grids = read_input()
    masks = [np.zeros_like(g, dtype=bool) for g in grids]

    done = False
    for num in bingo_input:
        for grid, mask in zip(grids, masks):
            mask |= grid == num

            if np.any(np.all(mask, axis=1)) or np.any(np.all(mask, axis=0)):
                done = True
                break

        if done:
            break
    print("Part 1:", np.sum(grid[~mask]) * num)


def solve_part_two():
    bingo_input, grids = read_input()
    masks = [np.zeros_like(g, dtype=bool) for g in grids]

    when_done = np.full(len(masks), len(masks))
    for i_input, num in enumerate(bingo_input):
        for i, (grid, mask) in enumerate(zip(grids, masks)):
            if when_done[i] < len(masks):
                continue

            mask |= grid == num

            if np.any(np.all(mask, axis=1)) or np.any(np.all(mask, axis=0)):
                when_done[i] = i_input

    imax = np.argmax(when_done)
    grid, mask = grids[imax], masks[imax]
    print("Part 2:", np.sum(grid[~mask]) * bingo_input[when_done[imax]])


solve_part_one()
solve_part_two()
