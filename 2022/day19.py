import re
from collections import defaultdict
from pathlib import Path

import joblib
import numpy as np

LINE_RE = re.compile(
    "Blueprint (?P<id>\d+): "
    "Each ore robot costs (?P<ore>\d+) ore. "
    "Each clay robot costs (?P<clay>\d+) ore. "
    "Each obsidian robot costs (?P<obs_ore>\d+) ore and (?P<obs_clay>\d+) clay. "
    "Each geode robot costs (?P<geode_ore>\d+) ore and (?P<geode_obs>\d+) obsidian."
)


def read_blueprints():
    raw_input = (
        "Blueprint 1: "
        "Each ore robot costs 4 ore. "
        "Each clay robot costs 2 ore. "
        "Each obsidian robot costs 3 ore and 14 clay. "
        "Each geode robot costs 2 ore and 7 obsidian."
        "\n"
        "Blueprint 2: "
        "Each ore robot costs 2 ore. "
        "Each clay robot costs 3 ore. "
        "Each obsidian robot costs 3 ore and 8 clay. "
        "Each geode robot costs 3 ore and 12 obsidian."
    )
    raw_input = (Path(__file__).parent / "input19").read_text()
    blueprints = []
    for line in raw_input.splitlines():
        data = {k: int(v) for k, v in LINE_RE.match(line).groupdict().items()}
        # Ore robot cost
        robot_costs = np.array(
            [
                [data["ore"], 0, 0, 0],  # ore robot
                [data["clay"], 0, 0, 0],  # clay robot
                [data["obs_ore"], data["obs_clay"], 0, 0],  # obsydian robot
                [data["geode_ore"], 0, data["geode_obs"], 0],  # geode-breaking robot
            ]
        )

        blueprints.append(robot_costs)

    return blueprints


def update_stock_and_fork(
    blueprint: np.ndarray,
    stock: np.ndarray,
    robots: np.ndarray,
    stacks: dict,
    time: int,
):
    for i in range(4):
        # Already maxed-out production of this item
        if i < 3 and robots[i] >= blueprint[:, i].max():
            continue
        cost = blueprint[i]

        mask = cost > 0

        if np.any(robots[mask] == 0):
            continue
        else:
            dt = int(max(0, np.ceil(np.max((cost - stock)[mask] / robots[mask]))))

        if time + dt >= 24:
            continue

        new_stock = stock + robots * (dt + 1) - cost
        new_robots = robots.copy()
        new_robots[i] += 1

        entry = tuple(new_stock), tuple(new_robots)

        if entry not in stacks[time + dt]:
            stacks[time + dt + 1].add(entry)

    # Simple production turn
    entry = tuple(stock + robots), tuple(robots)
    stacks[time + 1].add(entry)


def helper(ind_blueprint: int, blueprint: np.ndarray, tmax: int = 24) -> tuple[int, int]:
    robots = np.array([1, 0, 0, 0])
    stock = np.array([0, 0, 0, 0])

    stacks = defaultdict(set)
    stacks[0].add((tuple(stock), tuple(robots)))

    print(f"Blueprint #{ind_blueprint}:")
    for t in range(tmax+1):
        max_score = max(stock[3] for stock, _robot in stacks[t])
        max_prod = max(robots[3] for _stock, robots in stacks[t])

        filtered_stack = [
            (stock, robots)
            for stock, robots in stacks[t]
            if stock[3] > max_score - 2 and robots[3] > max_prod - 2
        ]

        print(
            f"{ind_blueprint:<4d}\t {t=} / {len(filtered_stack)}/{len(stacks[t])} / "
            f"{max_score=} {max_prod=}"
        )
        for s, r in filtered_stack:
            update_stock_and_fork(blueprint, np.asarray(s), np.asarray(r), stacks, t)

    return ind_blueprint, max_score


def part1():
    blueprints = read_blueprints()
    total_score = sum(
        ind * score
        for ind, score in 
        joblib.Parallel(n_jobs=30)(
            joblib.delayed(helper)(i + 1, blueprint)
            for i, blueprint in enumerate(blueprints)
        )
    )

    print("Total score:", total_score)

part1()
