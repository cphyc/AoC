import re

LINE_RE = re.compile(r"(\d+)-(\d+) (\w+): (\w+)")


def check_lines_v1(lines: list):
    Nok = 0
    for line in lines:
        grps = LINE_RE.match(line)
        if grps is None:
            raise RuntimeError()

        _nmin, _nmax, char, password = grps.groups()

        Nfound = password.count(char)

        nmin = int(_nmin)
        nmax = int(_nmax)

        if nmin <= Nfound <= nmax:
            Nok += 1

    return Nok


def check_lines_v2(lines: list):
    Nok = 0
    for line in lines:
        grps = LINE_RE.match(line)
        if grps is None:
            raise RuntimeError()
        _pos_1, _pos_2, char, password = grps.groups()

        pos_1 = int(_pos_1) - 1
        pos_2 = int(_pos_2) - 1

        Nok += (password[pos_1] == char) ^ (password[pos_2] == char)

    return Nok


with open("input") as f:
    lines = f.readlines()

print(check_lines_v1(lines))
print(check_lines_v2(lines))
