from typing import Iterable
from functools import reduce


def find_overlap(rucksack: str):
    mid = len(rucksack) // 2
    first = set(rucksack[:mid])
    second = set(rucksack[mid:])
    return find_item_in_common([first, second])


def find_item_in_common(rucksacks: list[str]) -> str:
    rucksacks_sets = list(map(set, rucksacks))
    common_item = reduce(lambda a, b: a & b, rucksacks_sets[1:], rucksacks_sets[0])
    return next(iter(common_item))


priorities = {chr(i): i - 96 for i in range(97, 123)}
priorities.update({chr(i): i - 38 for i in range(65, 91)})


def calc_priority(item: str):
    return priorities[item]


def read_rucksacks(file_name: str) -> list[str]:
    with open(file_name, "rt") as f:
        for line in f:
            yield line.strip()


def test1():
    rucksacks = [
        "vJrwpWtwJgWrhcsFMMfFFhFp",
        "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
        "PmmdzqPrVvPwwTWBwg",
        "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
        "ttgJtRGJQctTZtZT",
        "CrZsJsPPZsGzwwsLwLmpwMDw",
    ]
    assert sum(map(calc_priority, map(find_overlap, rucksacks))) == 157


def part1():
    return sum(
        map(calc_priority, map(find_overlap, read_rucksacks("input/day3-part1.txt")))
    )


def read_three(rucksacks: Iterable[str]) -> tuple[str, str, str]:
    try:
        while True:
            yield (next(rucksacks), next(rucksacks), next(rucksacks))
    except:
        return


def test2():
    rucksacks = [
        "vJrwpWtwJgWrhcsFMMfFFhFp",
        "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
        "PmmdzqPrVvPwwTWBwg",
        "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
        "ttgJtRGJQctTZtZT",
        "CrZsJsPPZsGzwwsLwLmpwMDw",
    ]
    groups = map(list, read_three(iter(rucksacks)))
    group_badges = map(find_item_in_common, groups)
    group_priorities = map(calc_priority, group_badges)
    assert sum(group_priorities) == 70


def part2():
    rucksacks = read_rucksacks("input/day3-part1.txt")
    groups = map(list, read_three(iter(rucksacks)))
    group_badges = map(find_item_in_common, groups)
    group_priorities = map(calc_priority, group_badges)
    return sum(group_priorities)


if __name__ == "__main__":
    test1()
    print(part1())
    test2()
    print(part2())
