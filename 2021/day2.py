def parse_input(fname):
    with open(fname) as f:
        for line in f.readlines():
            if not line:
                continue
            cmd, str_val = line.split()
            val = int(str_val)

            yield {"forward": (val, 0), "down": (0, +val), "up": (0, -val)}[cmd]


def solve_part_one():
    x, y = 0, 0

    for dx, dy in parse_input("input_day2.txt"):
        x += dx
        y += dy
    print("Part 1: ", x * y)


def solve_part_two():
    x, y, aim = 0, 0, 0
    for dx, dy in parse_input("input_day2.txt"):
        if dx > 0:  # forward
            x += dx
            y += dx * aim
        else:  # change aim
            aim += dy
    print("Part 2: ", x * y)


solve_part_one()
solve_part_two()
