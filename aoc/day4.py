from typing import Iterable


def parse_assignment(assignment: str) -> tuple[str, str]:
    return assignment.split(",")


def parse_range_pair(range_pair: tuple[str, str]) -> tuple[set[int], set[int]]:
    return tuple(map(parse_range, range_pair))


def parse_range(section_range: str) -> set[int]:
    first, last = map(int, section_range.split("-"))
    return set(range(first, last + 1))


def first_contains_second(first: set[int], second: set[int]) -> bool:
    return (first & second) == second


def either_contain(section_assignment: tuple[set[int], set[int]]) -> bool:
    return first_contains_second(
        section_assignment[0], section_assignment[1]
    ) or first_contains_second(section_assignment[1], section_assignment[0])


def is_overlapping_assignment(section_assignment: tuple[set[int], set[int]]) -> bool:
    return len(section_assignment[0] & section_assignment[1]) > 0


def count_redundant(redundant_assignments: Iterable[bool]) -> int:
    return len([redundant for redundant in redundant_assignments if redundant == True])


def count_redundant_assignments(
    assignments: list[str], section_assignment_comparator
) -> int:
    range_pairs = map(parse_assignment, assignments)
    section_assignments = map(parse_range_pair, range_pairs)
    redundant_assignments = map(section_assignment_comparator, section_assignments)
    return count_redundant(redundant_assignments)


def test1():
    assignments = ["2-4,6-8", "2-3,4-5", "5-7,7-9", "2-8,3-7", "6-6,4-6", "2-6,4-8"]
    assert count_redundant_assignments(assignments, either_contain) == 2


def read_file(file_name: str) -> Iterable[str]:
    with open(file_name) as f:
        yield from (line.strip() for line in f)


def part1():
    assignments = read_file("input/day4-part1.txt")
    return count_redundant_assignments(assignments, either_contain)


def test2():
    assignments = ["2-4,6-8", "2-3,4-5", "5-7,7-9", "2-8,3-7", "6-6,4-6", "2-6,4-8"]
    assert count_redundant_assignments(assignments, is_overlapping_assignment) == 4


def part2():
    assignments = read_file("input/day4-part1.txt")
    return count_redundant_assignments(assignments, is_overlapping_assignment)


if __name__ == "__main__":
    test1()
    print(part1())
    test2()
    print(part2())
