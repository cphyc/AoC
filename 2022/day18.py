from pathlib import Path

import numpy as np

raw_input = (Path(__file__).parent / "input18").read_text()
_raw_input = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""

block = np.zeros((20, 20, 20), dtype=bool)
for line in raw_input.splitlines():
    x, y, z = (int(_) for _ in line.split(","))
    block[x, y, z] = True

block = np.pad(block, 1, constant_values=False)


def part1():
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

    print("Surface area of droplets:", Nfaces)


part1()
