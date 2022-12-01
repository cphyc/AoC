def read_input():
    calories_per_elf = [[]]
    for line in open("input1").readlines():
        line = line.strip()

        if not line:
            # New elf!
            calories_per_elf.append([])
            continue

        calories_per_elf[-1].append(int(line))

    return calories_per_elf


def part1():
    calories_per_elf = read_input()
    max_calories = 0

    for calories in calories_per_elf:
        max_calories = max(max_calories, sum(calories))

    print("Day 1, part 1:", max_calories)


part1()
