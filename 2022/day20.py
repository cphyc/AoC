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


def decrypt(encrypted: list[tuple[int, int]], rounds: int = 1):
    # Work on a copy
    decrypted = copy(encrypted)
    N = len(decrypted)

    for _ in range(rounds):
        for ind_val in encrypted:
            _, val = ind_val
            index = decrypted.index(ind_val)
            # Remove the index from the list
            decrypted.pop(index)
            # and insert it at the correct position
            decrypted.insert((index + val) % (N - 1), ind_val)

    return decrypted


def part1():
    decrypted = np.array(decrypt(values))[:, 1]
    i0 = np.argwhere(decrypted == 0)[0, 0]

    ipos = (i0 + np.array([1000, 2000, 3000])) % len(decrypted)
    print("Part 1:", tmp := decrypted[ipos], tmp.sum())


def part2():
    encrytion_key = 811589153
    encrypted_with_key = [(i, val * encrytion_key) for i, val in values]
    decrypted = np.array(decrypt(encrypted_with_key, rounds=10))[:, 1]
    i0 = np.argwhere(decrypted == 0)[0, 0]

    ipos = (i0 + np.array([1000, 2000, 3000])) % len(decrypted)
    print("Part 2:", tmp := decrypted[ipos], tmp.sum())


part1()
part2()
