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


def compute_scenic_score(tree_map: np.ndarray, i0: int, j0: int):
    i = i0 - 1

    directions = (
        (+1, 0),  # left
        (-1, 0),  # right
        (0, +1),  # up
        (0, -1),  # down
    )

    counts = [0, 0, 0, 0]
    for idir, dir in enumerate(directions):
        i, j = i0 + dir[0], j0 + dir[1]

        while 0 <= i < tree_map.shape[0] and 0 <= j < tree_map.shape[1]:

            counts[idir] += 1
            if tree_map[i, j] >= tree_map[i0, j0]:
                break

            i += dir[0]
            j += dir[1]

    return np.prod(counts)


def part2():
    tree_map = read_input()
    scenic_scores = np.zeros_like(tree_map)

    for i in range(1, tree_map.shape[0] - 1):
        for j in range(1, tree_map.shape[1] - 1):
            scenic_scores[i, j] = compute_scenic_score(tree_map, i, j)

    print("Part II, max scenic score:", scenic_scores.max())


part1()
part2()
