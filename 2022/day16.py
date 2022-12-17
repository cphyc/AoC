import re
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Iterator

import networkx as nx
from tqdm import tqdm

raw_input = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""
raw_input = (Path(__file__).parent / "input16").read_text()

# parse input
tunnels = {}
valves_reading = {}

LINE_SYNTAX = re.compile(
    r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (\w+(?:, \w+)*)"
)

for line in raw_input.splitlines():
    if match := LINE_SYNTAX.match(line):
        valve, flow_rate, tunnels_to = match.groups()
        tunnels[valve] = tunnels_to.split(", ")
        valves_reading[valve] = int(flow_rate)

valves = [valve for valve in valves_reading if valves_reading[valve] > 0]

# Build a graph
G = nx.DiGraph()
for ifrom, tunnels_to in tunnels.items():
    G.add_node(ifrom, flow_rate=valves_reading[ifrom])
    for ito in tunnels_to:
        G.add_edge(ifrom, ito)

current_best_flow_rate = 0
current_best_path = None

distance_graph = {}
for source, dists in nx.shortest_path_length(G):
    for dest, dist in dists.items():
        distance_graph[source, dest] = dist


@dataclass
class ValveInstance:
    valves_activated: list[str]
    flow_rate: int
    human_time: int

    def __post_init__(self):
        self.total_time = 30

    @property
    def current_time(self):
        return self.human_time

    @cached_property
    def potential_flowrate(self):
        closed_valves = set(valves) - set(self.valves_activated)

        flow_rate = self.flow_rate
        for valve in closed_valves:
            path_len = distance_graph[self.valves_activated[-1], valve]

            dt = self.current_time + path_len + 1

            if dt >= self.total_time:
                continue
            remaining_time = self.total_time - dt
            flow_rate += remaining_time * G.nodes[valve]["flow_rate"]
        return flow_rate

    def branch(self):
        global current_best_flow_rate, current_best_path
        # Explore all possible branches *leading to a closed valve*
        closed_valves = list(set(valves) - set(self.valves_activated))

        for valve in closed_valves:
            path_len = distance_graph[self.valves_activated[-1], valve]
            new_time = self.current_time + path_len + 1
            flow_rate = G.nodes[valve]["flow_rate"]
            new_flow = self.flow_rate + (self.total_time - new_time) * flow_rate
            vi = ValveInstance(
                valves_activated=self.valves_activated + [valve],
                flow_rate=new_flow,
                human_time=new_time,
            )

            if vi.flow_rate > current_best_flow_rate:
                current_best_flow_rate = vi.flow_rate
                current_best_path = vi.valves_activated

            if vi.potential_flowrate >= current_best_flow_rate:
                yield vi


def part1():
    vi = ValveInstance(valves_activated=["AA"], flow_rate=0, human_time=0)
    stack = list(vi.branch())

    while stack:
        # print("Current best:", current_best_flow_rate, current_best_path)
        path = stack.pop()
        for vi in path.branch():
            stack.append(vi)

    print(current_best_path)
    print("Saving the elephant, part I:", current_best_flow_rate)


# part1()
def part2():
    non_zero_valves = [
        valve for valve, reading in valves_reading.items() if reading > 0
    ]
    GG = nx.DiGraph()

    GG.add_weighted_edges_from(
        (
            (orig, dest, dist)
            for (orig, dest), dist in distance_graph.items()
            if orig in non_zero_valves and dest in non_zero_valves and orig != dest
        )
    )

    # Generate all possible paths of total length < 26
    def generate_all_possible_paths(
        all_nodes: set[str],
        distance_graph: dict[tuple[str, str], int],
        current_path: list[str],
        current_path_length: int,
    ) -> Iterator[list[str], None, None]:
        for other_node in all_nodes - set(current_path):
            if other_node in current_path:
                continue
            new_path_length = (
                current_path_length + distance_graph[current_path[-1], other_node]
            )
            if new_path_length < 26:
                new_path = current_path + [other_node]
                yield new_path, new_path_length

                yield from generate_all_possible_paths(
                    all_nodes,
                    distance_graph,
                    new_path,
                    new_path_length,
                )

    def compute_flow_from_path(path: list[str]):
        flow = 0
        current_time = 0
        for i in range(1, len(path)):
            current_time += distance_graph[path[i - 1], path[i]] + 1
            flow += valves_reading[path[i]] * (26 - current_time)
        return flow

    all_possible_paths = list(
        tqdm(
            generate_all_possible_paths(
                set(non_zero_valves),
                distance_graph,
                ["AA"],
                0,
            ),
            total=447854,
            desc="Possible paths",
        )
    )

    all_possible_paths_with_flow = [
        (path, compute_flow_from_path(path))
        for path, path_len in tqdm(all_possible_paths, desc="Computing flow")
    ]

    all_possible_paths_with_flow.sort(key=lambda x: x[1], reverse=True)

    current_best = 0
    for i, (human_path, flow_human) in enumerate(
        tqdm(all_possible_paths_with_flow, desc="Exploring paths")
    ):
        if flow_human < current_best / 2:
            continue
        for j in range(i + 1, len(all_possible_paths_with_flow)):
            elephant_path, flow_elephant = all_possible_paths_with_flow[j]

            if flow_human + flow_elephant < current_best:
                break

            if set(human_path[1:]) & set(elephant_path[1:]):
                continue

            if flow_human + flow_elephant > current_best:
                current_best = flow_human + flow_elephant

    print("Saving the elephant, part II:", current_best)


part1()
part2()
