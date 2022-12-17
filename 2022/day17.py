from pathlib import Path
from typing import Generator

import numpy as np

rocks = [
    np.array(
        [
            [1, 1, 1, 1],
        ],
        dtype=bool,
    ),
    np.array(
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ],
        dtype=bool,
    ),
    np.array(
        [
            [0, 0, 1],
            [0, 0, 1],
            [1, 1, 1],
        ],
        dtype=bool,
    ),
    np.array(
        [
            [1],
            [1],
            [1],
            [1],
        ],
        dtype=bool,
    ),
    np.array(
        [
            [1, 1],
            [1, 1],
        ],
        dtype=bool,
    ),
]


def wind_direction() -> Generator[int, None, None]:
    # wind_directions_raw = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
    wind_directions_raw = (Path(__file__).parent / "input17").read_text().strip()
    i = 0
    while True:
        d = wind_directions_raw[i % len(wind_directions_raw)]
        yield (1 if d == ">" else -1)
        i += 1


def spawn_rock() -> Generator[np.ndarray, None, None]:
    i = 0
    while True:
        yield rocks[i % len(rocks)]
        i += 1


def simulate_rock(
    ground: np.ndarray[bool],
    rock: np.ndarray[bool],
    wind_blower: Generator[int, None, None],
    verbose=False,
):
    rock = rock[::-1]  # transpose rock so that y is increasing
    # ground has shape (..., 7)
    top_level = np.argmin(np.any(ground, axis=1))

    y, x = [top_level + 3, 2]
    H, W = rock.shape

    while True:
        wind = next(wind_blower)

        # Do one wind gust
        new_x = x + wind

        if (
            (new_x + W > 7)
            or (new_x < 0)  # hitting right wall
            or  # hitting left wall
            # Collision after wind, stopping there
            np.any(ground[y : y + H, new_x : new_x + W] & rock)
        ):
            new_x = x

        x = new_x

        # Do one move down
        new_y = y - 1
        if new_y < 0:
            # hit the ground
            break
        elif np.any(ground[new_y : new_y + H, x : x + W] & rock):
            # collision
            break

        y = new_y
        # print(x, y)

    ground[y : y + H, x : x + W] |= rock

    if verbose:
        for iy in range(top_level + H - 1, -1, -1):
            print("|" + "".join(np.where(ground[iy], "#", ".")) + "|")
        print("+-------+")


def part1():
    ground = np.zeros((10000, 7), dtype=bool)

    wind_blower = wind_direction()

    rock_spawner = spawn_rock()
    year = 0
    while year < 2022:
        simulate_rock(ground, next(rock_spawner), wind_blower, verbose=False)
        year += 1

    print("After 2022 falls, the height is", np.argmin(np.any(ground, axis=1)))
