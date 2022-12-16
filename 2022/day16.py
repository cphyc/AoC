import re
from dataclasses import dataclass
from importlib.resources import read_text
from pathlib import Path

import networkx as nx

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

print(tunnels)
print(valves_reading)

# Build a graph
G = nx.DiGraph()
for ifrom, tunnels_to in tunnels.items():
    G.add_node(ifrom, flow_rate=valves_reading[ifrom])
    for ito in tunnels_to:
        G.add_edge(ifrom, ito)

current_best_flow_rate = 0
current_best_path = None


@dataclass
class ValveInstance:
    valves_activated: list[str]
    flow_rate: int
    current_time: int

    def potential_flowrate(self):
        closed_valves = set(valves) - set(self.valves_activated)

        flow_rate = self.flow_rate
        for valve in closed_valves:
            path_len = nx.shortest_path_length(G, self.valves_activated[-1], valve)
            remaining_time = 30 - (self.current_time + path_len + 1)
            flow_rate += remaining_time * G.nodes[valve]["flow_rate"]
        return flow_rate

    def branch(self):
        global current_best_flow_rate, current_best_path
        # Explore all possible branches *leading to a closed valve*
        closed_valves = list(set(valves) - set(self.valves_activated))

        for valve in closed_valves:
            path_len = nx.shortest_path_length(G, self.valves_activated[-1], valve)
            new_time = self.current_time + path_len + 1
            flow_rate = G.nodes[valve]["flow_rate"]
            new_flow = self.flow_rate + (30 - new_time) * flow_rate
            vi = ValveInstance(
                valves_activated=self.valves_activated + [valve],
                flow_rate=new_flow,
                current_time=new_time,
            )

            if vi.flow_rate > current_best_flow_rate:
                current_best_flow_rate = vi.flow_rate
                current_best_path = vi.valves_activated

            if vi.potential_flowrate() >= current_best_flow_rate:
                yield vi


vi = ValveInstance(valves_activated=["AA"], flow_rate=0, current_time=0)
stack = list(vi.branch())

while stack:
    print("Current best:", current_best_flow_rate, current_best_path)
    path = stack.pop()
    for vi in path.branch():
        stack.append(vi)

print(current_best_flow_rate)
print(current_best_path)
