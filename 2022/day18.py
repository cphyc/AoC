from itertools import product
from pathlib import Path

import numpy as np

raw_input = (Path(__file__).parent / "input18").read_text()


block = np.zeros((20, 20, 20), dtype=bool)
for line in raw_input.splitlines():
    x, y, z = (int(_) for _ in line.split(","))
    block[x, y, z] = True

block = np.pad(block, 1, constant_values=False)


def count_faces_on_block(block: np.ndarray) -> int:
    sl_L, sl_R = slice(1, None), slice(None, -1)
    Nfaces = 0
    for idim in range(3):
        slices_L = tuple(slice(None) if i != idim else sl_L for i in range(3))
        slices_R = tuple(slice(None) if i != idim else sl_R for i in range(3))

        # Count faces within the block
        Nfaces += (block[slices_L] ^ block[slices_R]).sum()

        # Count faces on the boundary
        Nfaces += (
            block[:, :, 0].sum()
            + block[:, :, -1].sum()
            + block[:, 0, :].sum()
            + block[:, -1, :].sum()
            + block[0, :, :].sum()
            + block[-1, :, :].sum()
        )

    return Nfaces


def part1():
    Nfaces = count_faces_on_block(block)

    print("Surface area of droplets:", Nfaces)


part1()


def part2():
    # Trick here is to fill the airbubbles that aren't reachable from the outside
    new_block = block.copy() * 1

    new_block[0, :, :] = new_block[-1, :, :] = new_block[:, 0, :] = new_block[
        :, -1, :
    ] = new_block[:, :, 0] = new_block[:, :, -1] = 2
    # Expand region with 2s
    N = len(new_block)
    for _ in range(N // 2):
        tmp = new_block.copy()
        for i, j, k in product(range(1, N - 1), range(1, N - 1), range(1, N - 1)):
            if block[i, j, k]:
                new_block[i, j, k] = 1
                continue

            if (
                tmp[i - 1, j, k] == 2
                or tmp[i + 1, j, k] == 2
                or tmp[i, j - 1, k] == 2
                or tmp[i, j + 1, k] == 2
                or tmp[i, j, k - 1] == 2
                or tmp[i, j, k + 1] == 2
            ):
                new_block[i, j, k] = 2

    block_no_air = new_block < 2

    print("Surface area of droplets:", count_faces_on_block(block_no_air))


part2()
