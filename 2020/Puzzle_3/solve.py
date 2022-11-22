tree_map = open("input").readlines()


def throw_toboggan(right, down, tree_map):
    x = 0
    y = 0

    y_max = len(tree_map)
    x_max = len(tree_map[0]) - 1

    Nhit = 0
    while y < y_max:
        Nhit += tree_map[y][x % x_max] == "#"
        x += right
        y += down

    return Nhit


# Part 1 of the puzzle
print(throw_toboggan(right=3, down=1, tree_map=tree_map))

# Part 2 of the puzzle
slopes = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))

hit_product = 1
for right, down in slopes:
    Nhit = throw_toboggan(right=right, down=down, tree_map=tree_map)
    hit_product *= Nhit

print(hit_product)
