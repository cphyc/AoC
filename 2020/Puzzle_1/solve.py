from itertools import combinations

import numpy as np
from numba import njit

inputs = np.loadtxt("input", dtype=int)


@njit
def sum_to(values, Ntosum, target):
    Nvalues = len(values)
    Nitertot = Nvalues**Ntosum
    for i in range(Nitertot):
        iiprev = Nvalues
        s = 0
        ok = True
        i0 = i
        for _ in range(Ntosum):
            ii = i % Nvalues
            i //= Nvalues
            if ii > iiprev:
                ok = False
                break
            s += values[ii]
            if s > target:
                ok = False
                break
            iiprev = ii

        if ok and s == target:
            all_i = []
            for _ in range(Ntosum):
                all_i.append(i0 % Nvalues)
                i0 //= Nvalues
            return all_i
    else:
        return []


def sum_to_slow(values, Ntosum, target):
    for indices in combinations(range(len(values)), Ntosum):
        sigma = 0
        for i in indices:
            sigma += values[i]
            if sigma > target:
                break

        if sigma == target:
            return indices


def solve(values, Ntosum, target):
    indices = sum_to(values, Ntosum, target)

    vals = np.array([values[i] for i in indices])
    s = " + ".join(str(v) for v in vals)
    s += f" = {vals.sum()}"
    print(s)

    s = " * ".join(str(v) for v in vals)
    s += f" = {np.product(vals)}"
    print(s)
