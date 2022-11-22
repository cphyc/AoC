import re
from typing import AnyStr

FOUR_DIGITS = re.compile(r"^\d{4}$")


def n_digits(val, n, vmin, vmax):
    if re.match(rf"^\d{{{n}}}$", val):
        int_val = int(val)
        return vmin <= int_val <= vmax
    else:
        return False


def check_height(val: str):
    if val.endswith("cm"):
        return n_digits(val.replace("cm", ""), 3, 150, 193)
    elif val.endswith("in"):
        return n_digits(val.replace("in", ""), 2, 59, 76)
    else:
        return False


def check_hair_color(val: str):
    return re.match(r"^#[0-9a-f]{6}$", val) is not None


def check_eye_color(val: str):
    return val in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")


def parse_lines(lines: list[AnyStr]):
    data = {}
    for line in (_.strip() for _ in lines):
        if line == "":
            yield data
            data = {}
            continue
        for entry in line.strip().split(" "):
            key, value = entry.split(":")
            data[key] = value

    yield data


def check_data(data: dict, use_validators=False):
    validators = {
        "byr": lambda v: n_digits(v, 4, 1920, 2002),
        "iyr": lambda v: n_digits(v, 4, 2010, 2020),
        "eyr": lambda v: n_digits(v, 4, 2020, 2030),
        "hgt": check_height,
        "hcl": check_hair_color,
        "ecl": check_eye_color,
        "pid": lambda v: n_digits(v, 9, 0, 10**10 - 1),
    }

    for ek, is_valid in validators.items():
        if ek not in data:
            return False
        elif use_validators and not is_valid(data[ek]):
            return False
    else:
        return True


def check_input(lines, use_validators=False):
    return sum(check_data(dt, use_validators) for dt in parse_lines(lines))


lines = open("input_example").readlines()

for data in parse_lines(lines):
    print(f"{data}: {check_data(data)}")

lines = open("input").readlines()
print(f"Input has {check_input(lines)} valid passports.")

lines = open("input").readlines()
print(f"Input has {check_input(lines, True)} valid passports.")
