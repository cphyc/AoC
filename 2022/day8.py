from pathlib import Path

import numpy as np


def read_input():
    raw_data = (Path(__file__).parent / "input8").read_text().splitlines()
    return np.array([[int(x) for x in line] for line in raw_data])


def part1():
    tree_map = read_input()
    # Find whether a given tree is visible from outside the grid
    visibility_map = np.zeros_like(tree_map, dtype=bool)

    # Mark the edges
    visibility_map[0, :] = True
    visibility_map[-1, :] = True
    visibility_map[:, 0] = True
    visibility_map[:, -1] = True

    for i in range(1, tree_map.shape[0] - 1):
        for j in range(1, tree_map.shape[1] - 1):
            visibility_map[i, j] = (
                all(tree_map[i, j] > tree_map[:i, j])
                or all(tree_map[i, j] > tree_map[i + 1 :, j])  # left
                or all(tree_map[i, j] > tree_map[i, :j])  # right
                or all(tree_map[i, j] > tree_map[i, j + 1 :])  # up  # down
            )

    print("Part I, visible trees:", visibility_map.sum())


part1()
