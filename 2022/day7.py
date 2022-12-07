from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from textwrap import indent
from typing import Optional


@dataclass
class Node:
    children: dict[str, "Node"]
    self_size: int
    parent: Optional["Node"] = None

    def calc_size(self):
        return self.self_size + sum(
            child.calc_size() for child in self.children.values()
        )

    def traverse(self, callback: Callable, fullpath=None):
        if fullpath is None:
            fullpath = Path()
        for dirname, child_node in self.children.items():
            callback(child_node, fullpath / dirname)
            if not isinstance(child_node, Directory):
                continue
            child_node.traverse(callback, fullpath / dirname)

    def __repr__(self):
        child_repr = indent(
            "\n".join(f"{name}: {child!r}" for name, child in self.children.items()),
            "  | ",
        )
        if child_repr.strip():
            child_repr = "\n" + child_repr

        self_size = self.self_size
        calc_size = self.calc_size()

        return f"{self.__class__.__name__}: {self_size} {calc_size}{child_repr}"


class Directory(Node):
    pass


class File(Node):
    pass


def read_input():
    #     data = """\
    # $ cd /
    # $ ls
    # dir a
    # 14848514 b.txt
    # 8504156 c.dat
    # dir d
    # $ cd a
    # $ ls
    # dir e
    # 29116 f
    # 2557 g
    # 62596 h.lst
    # $ cd e
    # $ ls
    # 584 i
    # $ cd ..
    # $ cd ..
    # $ cd d
    # $ ls
    # 4060174 j
    # 8033020 d.log
    # 5626152 d.ext
    # 7214296 k"""
    data = (Path(__file__).parent / "input7").read_text()
    root = node = Node({"/": Directory({}, 0)}, 0)

    for line in data.splitlines():
        match line.split():
            case ["$", "ls"]:
                # Handle ls
                pass
            case ["$", "cd", ".."]:
                node = node.parent
            case ["$", "cd", directory]:
                node = node.children.get(directory, Directory({}, 0, node))
            case ["dir", directory]:
                node.children[directory] = Directory({}, 0, node)
            case [size_str, filename] if size_str.isnumeric():
                size = int(size_str)
                node.children[filename] = File({}, size, node)
            case _:
                raise ValueError(f"Invalid line: {line}")

    return root


def part1():
    tree = read_input()
    total_weight = 0

    def compute_weight(node: Node, fullpath: Path):
        nonlocal total_weight
        if isinstance(node, Directory) and (w := node.calc_size()) <= 100000:
            print(f"Adding {fullpath} with weight {w} to total weight")
            total_weight += w

    tree.traverse(compute_weight)
    print("Part I, total weight:", total_weight)


def part2():
    tree = read_input()

    available_diskpace = 70000000
    required_diskpace = 30000000

    current_free_diskpace = available_diskpace - tree.calc_size()
    need_to_be_freed = required_diskpace - current_free_diskpace

    candidates = []

    def find_candidates_for_deletion(node: Node, fullpath: Path):
        nonlocal candidates
        if isinstance(node, Directory) and (w := node.calc_size()) >= need_to_be_freed:
            print(
                f"Deleting {fullpath} with weight {w} would lead to"
                " {current_free_diskpace + w} free disk space"
            )
            candidates.append(w)

    tree.traverse(find_candidates_for_deletion)
    print("Part II, minimal folder to delete has size: ", min(candidates))


part1()
part2()
