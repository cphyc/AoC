from collections import defaultdict, namedtuple

import numpy as np

Instruction = namedtuple("Instruction", ("code", "val", "line"))
Edge = namedtuple("Edge", ("l", "instruction"))


def make_link(tree, inst, fp, instructions, all_instructions):
    new_fp = fp + inst.val if inst.code == "jmp" else fp + 1
    if new_fp >= len(instructions):
        # Reach beyond last instructions, do not create invalid link
        return
    next_inst = instructions[new_fp]

    all_instructions.add(inst)
    all_instructions.add(next_inst)

    edge = Edge(1, next_inst)
    tree[inst].append(edge)


def find_shortest_path(tree, instructions, all_instructions):
    # Create a graph
    for fp, inst in enumerate(instructions):
        make_link(tree, inst, fp, instructions, all_instructions)

        if inst.code != "acc":
            new_code = "jmp" if inst.code == "nop" else "nop"
            inst2 = Instruction(new_code, *inst[1:])

            edge = Edge(len(instructions), inst2)
            all_instructions.add(inst2)
            tree[inst].append(edge)

            make_link(tree, inst2, fp, instructions, all_instructions)

    # Initialize search
    nodes = all_instructions
    dist = {k: 2**30 for k in nodes}
    prev_node = {k: None for k in nodes}

    dist[instructions[0]] = 0
    node_queue = [(dist[node], node) for node in nodes]

    # Dijsktra algorithm (could be optimized with a queue)
    while len(node_queue) > 0:
        imin = np.argmin([d for d, _ in node_queue])
        d, u = node_queue.pop(imin)

        if u.code == "END":
            break

        edges = tree[u]
        for edge in edges:
            v = edge.instruction
            alt_dist = dist[u] + edge.l
            old_dist = dist[v]
            if alt_dist < old_dist:
                v_index = [instr for _, instr in node_queue].index(v)
                node_queue.pop(v_index)
                # heapify(node_queue)
                dist[v] = alt_dist
                prev_node[v] = u
                node_queue.append((alt_dist, v))
                # heappush(node_queue, (alt_dist, v))

    # Reconstruct the instruction list with the distances (to check)
    u = instructions[-1]
    op_list = []
    while u is not None:
        op_list.append((dist[u], u))
        u = prev_node[u]
    op_list = list(reversed(op_list))

    return op_list


def execute_instructions(op_list: list[Instruction]):
    acc = 0
    for op in op_list:
        if op.code == "acc":
            acc += op.val

    return acc


def main():
    with open("input") as f:
        lines = f.readlines()

    instructions = []
    for iline, line in enumerate(lines):
        instructions.append(Instruction(line[:3], int(line[3:]), iline))
    instructions.append(Instruction("END", 0, iline))
    all_instructions: set[Instruction] = set()

    tree: dict[Instruction, list[Edge]] = defaultdict(list)
    ret = find_shortest_path(tree, instructions, all_instructions)
    dist, op_list = zip(*ret)

    print(execute_instructions(op_list))


if __name__ == "__main__":
    main()
