from typing import AnyStr


def parse_seat_loc(s: AnyStr):
    row, col = s[:7], s[7:]
    irow = int(row.replace("F", "0").replace("B", "1"), 2)
    icol = int(col.replace("L", "0").replace("R", "1"), 2)

    return irow, icol


def get_seat_id(s: AnyStr):
    irow, icol = parse_seat_loc(s)

    return (irow << 3) + icol


def puzzle_part_1(lines: list[AnyStr]):
    # Find the maximum set id value
    return max(map(get_seat_id, lines))


def puzzle_part_2(lines: list[AnyStr]):
    # Find my seat id, i.e. the missing one for which the next and previous seat
    # ids exist

    seat_ids = sorted(map(get_seat_id, lines))

    for i, (s1, s2) in enumerate(zip(seat_ids[1:], seat_ids[:-1])):
        if s1 - s2 != 1:
            break

    return (s1 + s2) // 2


lines = [line.strip() for line in open("input").readlines()]

print(f"The maximum seat id is: {puzzle_part_1(lines)}")
print(f"My seat is: {puzzle_part_2(lines)}")
