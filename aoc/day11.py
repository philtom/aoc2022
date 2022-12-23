import collections
import dataclasses
import functools
import itertools
import re
from typing import Callable, Iterator
from aoc import utils


@dataclasses.dataclass
class Monkey:
    id: int
    items: list[int]
    operation: Callable[[int], int]
    test: Callable[[int], int]


def make_monkeys(lines: Iterator[str]) -> list[Monkey]:
    monkeys = []
    while True:
        monkey_number = re.match("Monkey (\d+):", next(lines)).group(1)
        starting_items = list(
            map(
                lambda x: int(x.strip()),
                re.match("  Starting items: (.*)", next(lines)).group(1).split(","),
            )
        )
        operation = parse_operation(next(lines))
        test = parse_test(next(lines), next(lines), next(lines))
        monkeys.append(
            Monkey(
                id=monkey_number, items=starting_items, operation=operation, test=test
            )
        )
        if next(lines, None) is None:
            return monkeys


def parse_operation(line: str) -> Callable[[int], int]:
    match = re.match("  Operation: new = old ([+*]) ([\d]+|old)", line)
    op = match.group(1)
    operand = match.group(2)
    # print(f"op: {op} operand: {operand}")
    if operand == "old":
        if op == "+":
            return lambda old: old + old
        elif op == "*":
            return lambda old: old * old
    else:
        if op == "+":
            return lambda old: old + int(operand)
        elif op == "*":
            return lambda old: old * int(operand)

    raise Exception(f"Unhandled operation: {line}")


def parse_test(test: str, if_true: str, if_false: str) -> int:
    operand = int(re.match("  Test: divisible by (\d+)", test).group(1))
    dest_true = int(re.match("    If true: throw to monkey (\d+)", if_true).group(1))
    dest_false = int(re.match("    If false: throw to monkey (\d+)", if_false).group(1))
    return lambda item: dest_true if item % operand == 0 else dest_false


def evaluate_monkeys(monkeys: list[Monkey]) -> list[Monkey]:
    #   for each monkey
    return map(lambda monkey: evaluate_monkey(monkey, monkeys), monkeys)


def evaluate_monkey(monkey: Monkey, initial_monkeys: list[Monkey]) -> list[Monkey]:
    #     for each item
    # print(f"monkey: {monkey}")
    return functools.reduce(
        lambda monkeys, item: evaluate_item(item, monkey, monkeys),
        monkey.items,
        initial_monkeys,
    )


def evaluate_item(item: int, monkey: Monkey, monkeys: list[Monkey]) -> list[Monkey]:
    new_worry_level = monkey.operation(item) // 3
    catching_monkey = monkey.test(new_worry_level)
    monkeys[catching_monkey].items.append(new_worry_level)
    return monkeys


def monkey_around(initial_monkeys: list[Monkey], rounds: int) -> dict[int, int]:
    # return functools.reduce(lambda monkeys, round: evaluate_monkeys(monkeys), range(0, rounds), initial_monkeys)
    # for each round
    inspection_counts = collections.defaultdict(int)
    for round in range(0, rounds):
        for monkey in initial_monkeys:
            while monkey.items:
                inspection_counts[monkey.id] += 1
                item = monkey.items.pop(0)
                new_worry_level = monkey.operation(item) // 3
                catching_monkey = monkey.test(new_worry_level)
                initial_monkeys[catching_monkey].items.append(new_worry_level)
                # print(f"round {round}")
                # for monkey in initial_monkeys:
                #     print(monkey.items)
    return inspection_counts

    # return initial_monkeys
    #       operation(item)
    #       divide by 3, round down
    #       test and throw


def test1():
    input = utils.read_input("input/day11-part1-test.txt")
    monkeys = make_monkeys(input)
    inspections_counts = monkey_around(monkeys, 20)
    top_two = sorted(inspections_counts.values())[-2:]
    monkey_business = top_two[0] * top_two[1]
    assert monkey_business == 10605

def part1():
    input = utils.read_input("input/day11-part1.txt")
    monkeys = make_monkeys(input)
    inspections_counts = monkey_around(monkeys, 20)
    top_two = sorted(inspections_counts.values())[-2:]
    monkey_business = top_two[0] * top_two[1]
    print(monkey_business)
    assert monkey_business == 55458

def main():
    test1()
    part1()


if __name__ == "__main__":
    main()
