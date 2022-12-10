from typing import Iterator
from aoc import utils
import collections
import re
from functools import partial

# read input
# read stacks
# read moves
def read_stack_input(input: Iterator[str]) -> list[str]:
    lines = []
    for line in input:
        if line.strip() == "":
            break
        lines.append(line)
    return lines


def parse_stack_input(stack_input: list[str]) -> list[collections.deque]:
    reversed_stack_input = reversed(stack_input)
    names_input = next(reversed_stack_input)
    stacks = {int(name): collections.deque() for name in get_groups(names_input)}
    for input in reversed_stack_input:
        i = 1
        for cargo_input in get_groups(input):
            cargo = parse_cargo_input(cargo_input)
            if cargo.strip() != "":
                stacks[i].append(parse_cargo_input(cargo_input))
            i += 1
    return stacks


def parse_cargo_input(cargo_input: str) -> str:
    # [x]
    return cargo_input[1]


def get_groups(line: str) -> Iterator[str]:
    for i in range(0, len(line), 4):
        yield line[i : i + 3]


def parse_move_input(inputs: Iterator[str]) -> tuple[int, int, int]:
    for line in inputs:
        # move 1 from 2 to 1
        m = re.search("move (\d+) from (\d+) to (\d+)", line)
        yield tuple(map(int, m.groups()))


def execute_move_with_stack(
    stacks: list[collections.deque], move: tuple[int, int, int]
):
    number = move[0]
    from_stack = move[1]
    to_stack = move[2]

    for i in range(0, number):
        stacks[to_stack].append(stacks[from_stack].pop())

    return stacks

def execute_grouped_move_with_stack(
    stacks: list[collections.deque], move: tuple[int, int, int]
):
    number = move[0]
    from_stack = move[1]
    to_stack = move[2]

    temp_stacks = collections.defaultdict(collections.deque)
    for i in range(0, number):
        temp_stacks[from_stack].append(stacks[from_stack].pop())


    for i in range(0, number):
        stacks[to_stack].append(temp_stacks[from_stack].pop())

    return stacks


def move_cargo_and_report_top_cargo(input: Iterator[str], move_fn) -> str:
    stack_input = read_stack_input(input)
    stacks = parse_stack_input(stack_input)
    moves = parse_move_input(input)
    for move in moves:
        move_fn(stacks, move)

    return "".join([stacks[key].pop() for key in sorted(list(stacks.keys()))])


def test1():
    input = utils.read_input("input/day5-part1-test.txt")
    assert move_cargo_and_report_top_cargo(input, execute_move_with_stack) == "CMZ"


def part1():
    input = utils.read_input("input/day5-part1.txt")
    return move_cargo_and_report_top_cargo(input, execute_move_with_stack)


def test2():
    input = utils.read_input("input/day5-part1-test.txt")
    assert move_cargo_and_report_top_cargo(input, execute_grouped_move_with_stack) == "MCD"

def part2():
    input = utils.read_input("input/day5-part1.txt")
    return move_cargo_and_report_top_cargo(input, execute_grouped_move_with_stack)


def main():
    test1()
    print(part1())
    test2()
    print(part2())
