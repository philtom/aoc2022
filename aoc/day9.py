import dataclasses
from functools import reduce
import itertools
from aoc import utils


@dataclasses.dataclass
class State:
    head_coord: tuple[int, int]
    tail_coord: tuple[int, int]
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
    return move_tail(move_head(state, direction))


def move_head(state: State, direction: str) -> State:
    if direction == "R":
        return dataclasses.replace(state, head_coord=move_right(state.head_coord))
    elif direction == "L":
        return dataclasses.replace(state, head_coord=move_left(state.head_coord))
    elif direction == "U":
        return dataclasses.replace(state, head_coord=move_up(state.head_coord))
    elif direction == "D":
        return dataclasses.replace(state, head_coord=move_down(state.head_coord))
    else:
        raise ValueError(f"Unknown direction: {direction}")


def move_tail(state: State) -> State:
    """
      H H H
    H . . . H
    H . T . H
    H . . . H
      H H H
    """
    delta_x = state.head_coord[0] - state.tail_coord[0]
    delta_y = state.head_coord[1] - state.tail_coord[1]
    if delta_x == 0 and delta_y == 0:
        return state

    new_coords = state.tail_coord
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

    return update_tail_coord(state, new_coords)


def move_up(coord: tuple[int, int]) -> tuple[int, int]:
    return (coord[0], coord[1] + 1)


def move_down(coord: tuple[int, int]) -> tuple[int, int]:
    return (coord[0], coord[1] - 1)


def move_right(coord: tuple[int, int]) -> tuple[int, int]:
    return (coord[0] + 1, coord[1])


def move_left(coord: tuple[int, int]) -> tuple[int, int]:
    return (coord[0] - 1, coord[1])


def update_tail_coord(state: State, tail_coord: tuple[int, int]) -> State:
    return dataclasses.replace(
        state, tail_coord=tail_coord, tail_history=state.tail_history | {tail_coord}
    )


def test1():
    inputs = utils.read_input("input/day9-part1-test.txt")
    state = reduce(
        process_input,
        inputs,
        State(head_coord=(0, 0), tail_coord=(0, 0), tail_history={(0, 0)}),
    )
    assert len(state.tail_history) == 13


def part1():
    inputs = utils.read_input("input/day9-part1.txt")
    state = reduce(
        process_input,
        inputs,
        State(head_coord=(0, 0), tail_coord=(0, 0), tail_history={(0, 0)}),
    )
    print(len(state.tail_history))
    assert len(state.tail_history) == 6367


def main():
    test1()
    part1()
