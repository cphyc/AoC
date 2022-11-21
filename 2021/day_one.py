import numpy as np

def solve_part_one():
    vals = np.loadtxt("./input_day1.txt")
    counts = np.sum(vals[1:] > vals[:-1])
    print("Part 1: ", counts)

def solve_part_two():
    vals = np.loadtxt("./input_day1.txt")
    threesome = vals[2:] + vals[1:-1] + vals[:-2]
    counts = np.sum(threesome[1:] > threesome[:-1])
    print("Part 2: ", counts)

solve_part_one()
solve_part_two()