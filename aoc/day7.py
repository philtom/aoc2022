from typing import Iterator
from aoc import utils, file_system
import more_itertools


def is_command(line: str) -> bool:
    return line.startswith("$")


def is_command_or_none(line: str) -> bool:
    return line is None or is_command(line)


def parse_command(line: str):
    tokens = line.split(" ")
    return tokens[1:]


def handle_command(
    tokens: list[str], lines: Iterator[str], current_directory: file_system.Directory
) -> file_system.Directory:
    command = tokens[0]

    if command == "cd":
        name = tokens[1]
        return file_system.change_directory(current_directory, name)

    elif command == "ls":
        while True:
            if is_command_or_none(lines.peek(None)):
                break
            line = next(lines)
            tokens = parse_listing(line)
            handle_listing(current_directory, tokens)
        return current_directory
    else:
        raise Exception(f"Unknown command: {command}")


def parse_listing(line: str) -> list[str]:
    return line.split(" ")


def handle_listing(
    current_directory: file_system.Directory, tokens: list[str]
) -> file_system.Directory:
    if tokens[0] == "dir":
        name = tokens[1]
        return file_system.make_directory(current_directory, name)
    else:
        size = int(tokens[0])
        name = tokens[1]
        return file_system.add_file(current_directory, name, size)


def build_file_system(lines: Iterator[str]) -> file_system.Directory:
    root = file_system.create_new_file_system()
    current_directory = root
    for line in lines:
        if is_command(line):
            tokens = parse_command(line)
            current_directory = handle_command(tokens, lines, current_directory)
    return root


def sum_directories_less_than_or_equals(
    directory: file_system.Directory, max_size: int
) -> int:
    directories = file_system.find_directories(directory)
    total_sizes = map(file_system.calc_total_size, directories)
    return sum(total_size for total_size in total_sizes if total_size <= max_size)


def test1():
    lines = more_itertools.peekable(utils.read_input("input/day7-part1-test.txt"))
    root = build_file_system(lines)
    assert file_system.calc_total_size(root) == 48381165
    total_size_at_most_100k = sum_directories_less_than_or_equals(root, 100000)
    assert total_size_at_most_100k == 95437


def part1():
    lines = more_itertools.peekable(utils.read_input("input/day7-part1.txt"))
    root = build_file_system(lines)
    total_size_at_most_100k = sum_directories_less_than_or_equals(root, 100000)
    print(total_size_at_most_100k)
    assert total_size_at_most_100k == 1778099

def test2():
    lines = more_itertools.peekable(utils.read_input("input/day7-part1-test.txt"))
    root = build_file_system(lines)
    directories = file_system.find_directories(root)
    directory_sizes = {directory.name:file_system.calc_total_size(directory) for directory in directories}
    total_disk_available = 70000000
    required_unused_space = 30000000
    unused_space = total_disk_available - directory_sizes["/"]
    space_to_delete = required_unused_space - unused_space
    deletion_candidate_sizes = [size for name, size in directory_sizes.items() if size >= space_to_delete]
    smallest_size = sorted(deletion_candidate_sizes)[0]
    assert smallest_size == 24933642

def main():
    test1()
    part1()
    test2()
