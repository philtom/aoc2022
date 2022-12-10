from typing import Iterable, Iterator
from functools import reduce


def read_input(file_name: str) -> Iterator[str]:
    with open(file_name, "rt") as f:
        for line in f:
            yield line.strip()


def collect_calories(calories: Iterator[str]) -> list[str]:
    def collect(acc: list[int], x: str):
        if x != "":
            acc[-1] += int(x)
        else:
            acc.append(0)
        return acc

    return reduce(collect, calories, [0])


def run(file_name: str):
    calories_per_elf = []
    with open(file_name, "rt") as f:
        total = 0
        for line in f:
            line = line.strip()
            if line == "":
                calories_per_elf.append(total)
                total = 0
            else:
                total += int(line)
    return max(calories_per_elf)


def part1(file_name: str):
    return max(collect_calories(read_input(file_name)))


def part2(file_name: str):
    return sum(sorted(collect_calories(read_input(file_name)))[-3:])


if __name__ == "__main__":
    print(part1("input/day1.txt"))
    print(part2("input/day1.txt"))
