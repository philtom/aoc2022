import functools
import itertools
from typing import Iterator
from aoc import utils


def create_grid(lines: str) -> list[list[int]]:
    grid = []
    row_index = 0
    for line in lines:
        grid.append([])
        col_index = 0
        for i in line:
            grid[row_index].append(int(i))
            col_index += 1
        row_index += 1
    return grid


def is_visible(grid: list[list[int]], row: int, col: int) -> bool:
    # edges are visible
    if row == 0 or col == 0:
        return True

    # edges are visible
    row_count = len(grid)
    col_count = len(grid[0])
    if row == row_count - 1 or col == col_count - 1:
        return True

    height = grid[row][col]

    def is_visible_from_edge(coordinates: Iterator[tuple[int, int]]) -> bool:
        hidden = any(map(lambda rc: grid[rc[0]][rc[1]] >= height, coordinates))
        return not hidden

    return is_visible_from_edge(
            itertools.product(range(0, row), [col])
        ) or is_visible_from_edge(
            itertools.product(range(row + 1, row_count), [col])
        ) or is_visible_from_edge(
            itertools.product([row], range(0, col))
        ) or is_visible_from_edge(
            itertools.product([row], range(col + 1, col_count))
        ) 
    


def count_visible(grid: list[list[int]]) -> int:
    row_count = len(grid)
    col_count = len(grid[0])

    def _is_visible(rc: tuple[int, int]) -> bool:
        return is_visible(grid, rc[0], rc[1])

    visibilities = map(
        _is_visible, itertools.product(range(0, row_count), range(0, col_count))
    )
    return sum(1 for visibile in visibilities if visibile)


def test1():
    input = utils.read_input("input/day8-part1-test.txt")
    grid = create_grid(input)
    assert count_visible(grid) == 21


def main():
    test1()
