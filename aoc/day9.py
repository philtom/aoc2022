import dataclasses
from functools import reduce
import itertools
from typing import Iterator
from aoc import utils


@dataclasses.dataclass
class State:
    knot_coords: list[tuple[int, int]]
    tail_history: set[tuple[int, int]]


@dataclasses.dataclass
class Move:
    direction: str
    distance: int


def parse_move(input: str) -> Move:
    tokens = input.split(" ")
    return Move(tokens[0], int(tokens[1]))


def process_input(state: State, input: str) -> State:
    move = parse_move(input)
    return reduce(
        process_move_increment, itertools.repeat(move.direction, move.distance), state
    )


def process_move_increment(state: State, direction: str) -> State:
    new_head = move(state.knot_coords[0], direction)
    # new_coords = list(map(follow, pairs(iter(state.knot_coords))))
    def follow_each(coords, i):
        return coords[:i] + [follow((coords[i - 1], coords[i]))] + coords[i+1:]

    new_coords = reduce(
        follow_each,
        range(1, len(state.knot_coords)),
        [new_head] + state.knot_coords[1:],
    )
    state = dataclasses.replace(
        state,
        knot_coords=new_coords,
        tail_history=state.tail_history | {new_coords[-1]},
    )
    return state


def pairs(
    elements: Iterator[tuple[int, int]]
) -> Iterator[tuple[tuple[int, int], tuple[int, int]]]:
    prev = next(elements)
    curr = next(elements)
    while curr:
        yield (prev, curr)
        prev = curr
        curr = next(elements, None)


def move(coord: tuple[int, int], direction: str) -> tuple[int, int]:
    if direction == "R":
        return move_right(coord)
    elif direction == "L":
        return move_left(coord)
    elif direction == "U":
        return move_up(coord)
    elif direction == "D":
        return move_down(coord)
    else:
        raise ValueError(f"Unknown direction: {direction}")


def follow(pair: tuple[tuple[int, int], tuple[int, int]]) -> tuple[int, int]:
    leader, follower = pair
    delta_x = leader[0] - follower[0]
    delta_y = leader[1] - follower[1]

    new_coords = follower
    if delta_y == 2 or (delta_y == 1 and abs(delta_x) == 2):
        # move up
        new_coords = move_up(new_coords)

    if delta_y == -2 or (delta_y == -1 and abs(delta_x) == 2):
        # move down
        new_coords = move_down(new_coords)

    if delta_x == 2 or (delta_x == 1 and abs(delta_y) == 2):
        # move right
        new_coords = move_right(new_coords)

    if delta_x == -2 or (delta_x == -1 and abs(delta_y) == 2):
        # move left
        new_coords = move_left(new_coords)

    return new_coords


def move_up(coord: tuple[int, int]) -> tuple[int, int]:
    return (coord[0], coord[1] + 1)


def move_down(coord: tuple[int, int]) -> tuple[int, int]:
    return (coord[0], coord[1] - 1)


def move_right(coord: tuple[int, int]) -> tuple[int, int]:
    return (coord[0] + 1, coord[1])


def move_left(coord: tuple[int, int]) -> tuple[int, int]:
    return (coord[0] - 1, coord[1])


def test1():
    inputs = utils.read_input("input/day9-part1-test.txt")
    state = reduce(
        process_input,
        inputs,
        State(
            knot_coords=[(0, 0), (0, 0)],
            tail_history={(0, 0)},
        ),
    )
    assert len(state.tail_history) == 13


def part1():
    inputs = utils.read_input("input/day9-part1.txt")
    state = reduce(
        process_input,
        inputs,
        State(
            knot_coords=[(0, 0), (0, 0)],
            tail_history={(0, 0)},
        ),
    )
    print(len(state.tail_history))
    assert len(state.tail_history) == 6367


def main():
    test1()
    part1()
