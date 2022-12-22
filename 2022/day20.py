from copy import copy
from pathlib import Path

import numpy as np

raw_input = """1
2
-3
3
-2
0
4"""

raw_input = (Path(__file__).parent / "input20").read_text()

values = [(i, int(line)) for i, line in enumerate(raw_input.splitlines())]


def decrypt(encrypted: list[tuple[int, int]]):
    # Work on a copy
    decrypted = copy(encrypted)
    N = len(decrypted)

    for ind_val in encrypted:
        _, val = ind_val
        index = decrypted.index(ind_val)
        # Remove the index from the list
        decrypted.pop(index)
        # and insert it at the correct position
        decrypted.insert((index + val) % (N - 1), ind_val)

    return decrypted


decrypted = np.array(decrypt(values))[:, 1]
i0 = np.argwhere(decrypted == 0)[0, 0]

print("Part 1:", tmp := np.roll(decrypted, -i0)[1000:3001:1000], tmp.sum())
