from pathlib import Path

import networkx as nx
import numpy as np

raw_input = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

raw_input = (Path(__file__).parent / "input12").read_text()

height_map = np.array(
    [[ord(c) - ord("a") for c in line] for line in raw_input.splitlines()]
)

for i, line in enumerate(raw_input.splitlines()):
    if "S" in line:
        start = (i, line.index("S"))
    if "E" in line:
        end = (i, line.index("E"))
height_map[start] = 0
height_map[end] = ord("z") - ord("a")


def add_edges(
    graph: nx.Graph,
    height_map: np.ndarray,
    i: int,
    j: int,
) -> None:
    for di, dj in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        i2, j2 = i + di, j + dj
        if 0 <= i2 < height_map.shape[0] and 0 <= j2 < height_map.shape[1]:
            if height_map[i2, j2] <= height_map[i, j] + 1:
                graph.add_edge((i, j), (i2, j2))


graph = nx.DiGraph()
for i in range(height_map.shape[0]):
    for j in range(height_map.shape[1]):
        graph.add_node((i, j))
for i in range(height_map.shape[0]):
    for j in range(height_map.shape[1]):
        add_edges(graph, height_map, i, j)

print(
    "Number of steps to reach best signal:", nx.shortest_path_length(graph, start, end)
)

print(
    "Minimal number of steps to reach best signal:",
    nx.multi_source_dijkstra(
        graph,
        [tuple(start_pt) for start_pt in np.argwhere(height_map == 0)],
        target=end,
    )[0],
)
