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


class WindManager:
    state: int
    cum_state: int

    def __iter__(self):
        # wind_directions_raw = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
        wind_directions_raw = (Path(__file__).parent / "input17").read_text().strip()
        self.state = 0
        self.cum_state = 0
        while True:
            d = wind_directions_raw[self.state % len(wind_directions_raw)]
            yield (1 if d == ">" else -1)
            self.state += 1
            self.state %= len(wind_directions_raw)
            self.cum_state += 1


def spawn_rock() -> Generator[np.ndarray, None, None]:
    i = 0
    Nrocks = len(rocks)
    while True:
        yield rocks[i]
        i += 1
        i %= Nrocks


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


def top_of_stack(ground: np.ndarray[bool]) -> int:
    return np.argmin(np.any(ground, axis=1))


def to_int(ground: np.ndarray[bool]) -> tuple[int, ...]:
    return tuple(int("".join(np.where(grd, "1", "0")), 2) for grd in ground)


def solve_for_year(tgt_year: int):
    ground = np.zeros((10000, 7), dtype=bool)

    Nrocks = len(rocks)
    wind_mgr = WindManager()
    wind_blower = iter(wind_mgr)

    stack_size = sum(rock.shape[0] for rock in rocks)

    rock_spawner = spawn_rock()
    year = 0
    stack_states: dict[tuple[int, tuple[int, ...]], tuple[int, int]] = {}
    fast_forward = True
    while year < tgt_year:
        simulate_rock(ground, next(rock_spawner), wind_blower, verbose=False)

        year += 1
        if year % Nrocks == (Nrocks - 1):
            cur_height = top_of_stack(ground)
            bottom = max(cur_height - stack_size, 0)

            wind_state = wind_mgr.state
            ground_signature = to_int(ground[bottom:cur_height])

            prev_occurence, prev_height = stack_states.get(
                (wind_state, ground_signature), (-1, -1)
            )
            if prev_occurence != -1 and fast_forward:
                print(
                    f"Stack is repeating from {prev_occurence=} to {year=}"
                    f"(Delta = {year - prev_occurence}, "
                    f"DeltaHeight = {cur_height - prev_height})"
                )
                Delta = year - prev_occurence
                DeltaHeight = cur_height - prev_height
                Nsteps = (tgt_year - year) // Delta
                new_year = year + Nsteps * Delta
                print(
                    f"Fast-forwarding from {year=} to {new_year=} "
                    f"(Nsteps={(new_year-year)/Delta}) wind state {wind_mgr.cum_state}"
                )
                year = new_year

                fast_forward = False

            stack_states[wind_state, ground_signature] = year, cur_height

    print(
        f"After {tgt_year} falls, the height is",
        top_of_stack(ground) + DeltaHeight * Nsteps,
    )


def part1():
    solve_for_year(2022)


def part2():
    solve_for_year(1_000_000_000_000)


part1()
print()
part2()
