from collections.abc import Callable

import numpy as np


def parse_rule(line: str) -> tuple[str, Callable]:
    name, rule_str = line.split(": ")

    def gen_range_matcher(vmin, vmax):
        def range_matcher(v):
            return vmin <= v <= vmax

        return range_matcher

    matchers = []
    for r in rule_str.split(" or "):
        vmin, vmax = (int(_) for _ in r.split("-"))
        tmp = gen_range_matcher(vmin, vmax)
        matchers.append(tmp)

    return name, lambda v: any(m(v) for m in matchers)


def check_ticket(ticket: list[int], rules: list) -> int:
    for i, value in enumerate(ticket):
        value_ok = any(rule(value) for rule in rules)
        if not value_ok:
            return i
    return -1


def find_valid_tickets(tickets, rules) -> list[int]:
    rules_list = list(rules.values())

    return [check_ticket(ticket, rules_list) for ticket in tickets]


def find_ok_rule_position(tickets, rules) -> dict[str, dict]:
    columns = zip(*tickets)

    # For each column, check which rules may apply
    ok: dict[str, dict] = {rule: {} for rule in rules.keys()}
    for icol, column in enumerate(columns):
        for rule_name, rule_fun in rules.items():
            ok[rule_name][icol] = all(rule_fun(c) for c in column)

    return ok


def swap(matrix, i, irow, icol):
    new_matrix = matrix.copy()
    new_matrix[[irow, i], :] = new_matrix[[i, irow], :]
    new_matrix[:, [icol, i]] = new_matrix[:, [i, icol]]
    return new_matrix


def find_combinations(ok_matrix):
    """
    ok_matrix: (Nrules+1 x Ncolumns+1) boolean array

    The last column contain the row index.
    The last row contain the column index.
    """
    N, M = ok_matrix.shape
    N -= 1
    M -= 1

    # Sort by number of ok entries
    counts = np.sum(ok_matrix[:N, :M], axis=1)
    iord = np.zeros_like(counts)
    iord[counts - 1] = np.arange(len(counts))
    ok_matrix[:N, :] = ok_matrix[iord, :]

    counts = 21 - np.sum(ok_matrix[:N, :M], axis=0)
    iord = np.zeros_like(counts)
    iord[counts - 1] = np.arange(len(counts))
    ok_matrix[:, :M] = ok_matrix[:, iord]
    return True, ok_matrix, 1

    def recursive(ok_matrix, i0, counts):
        if i0 == N - 1:
            return ok_matrix[i0, i0] == 1, ok_matrix, counts

        # Try out to move the columns so that [i0, i0] == 1
        for icol in np.where(ok_matrix[i0, i0:-1])[0]:
            counts += 1
            icol += i0
            print(" " * i0, f"Swapping {i0} <-> {icol}")
            tmp = ok_matrix.copy()
            tmp[:, [icol, i0]] = tmp[:, [i0, icol]]
            ok, new_ok_matrix, counts = recursive(tmp, i0 + 1, counts)

            if ok:
                return ok, new_ok_matrix, counts

    return recursive(ok_matrix, 0, 0)


if True:  # def main():
    lines = iter(open("input").readlines())

    line = next(lines)

    # Parse rules
    rules = {}
    while line != "\n":
        name, matcher = parse_rule(line)
        rules[name] = matcher
        line = next(lines)

    line = next(lines)
    # Parse my ticket
    line = next(lines)
    my_ticket = [int(_) for _ in line.split(",")]

    line = next(lines)
    # Parse my ticket
    line = next(lines)
    all_tickets = []
    for line in lines:
        all_tickets.append([int(_) for _ in line.split(",")])

    # Part I
    valids = find_valid_tickets(all_tickets, rules)
    p = sum(ticket[i] for ticket, i in zip(all_tickets, valids) if i > -1)

    print(f"Product of invalid items: {p}")

    # Part II
    valid_tickets = [tuple(t) for t, i in zip(all_tickets, valids) if i == -1]
    ok = find_ok_rule_position(valid_tickets, rules)
    Ncol = len(list(ok.values())[0])
    ok_matrix = np.concatenate(
        (
            [list(_.values()) + [0] for _ in ok.values()],
            [list(range(Ncol)) + [0]],
        ),
        axis=0,
    )
    ok_matrix[:, -1] = list(range(ok_matrix.shape[1]))
    ok_matrix[-1, -1] = ok_matrix.shape[0]  # large value so that we don't pick it up

    # okk, ret_matrix, count = find_combination2(ok_matrix.copy(), i)
    okk, ret_matrix, counts = find_combinations(ok_matrix.copy())
    print(ret_matrix)
    irules = ret_matrix[:-1, -1]
    icols = ret_matrix[-1, :-1]
    rule_names = np.array(list(ok.keys()))
    print(okk, counts)
    print(ret_matrix[:-1, :-1])
    print(rule_names[irules][np.argsort(icols)])

    rule_index = {
        rn: icol for icol, rn in enumerate(rule_names[irules][np.argsort(icols)])
    }

    print("Checking validity...", end="")
    for rn, icol in rule_index.items():
        assert ok[rn][icol], rn
    print(" ok!")

    p = 1
    for rn, icol in rule_index.items():
        if not rn.startswith("departure"):
            continue
        p *= my_ticket[icol]
    print(f"Product: {p}")
