"""
clock
op cycles_left
register
"""
import dataclasses
import functools
import itertools
from typing import Iterator
from aoc import utils


@dataclasses.dataclass
class State:
    clock: int
    register_x: int


def init_state():
    return State(clock=0, register_x=1)


def run_computer(instructions: Iterator[str]):
    register_x = 1
    op = None
    params = None
    cycles_left = None
    signals = []
    total_signal = 0
    clock = 0
    for clock in itertools.count(1):
        # get next op if ready
        if not op:
            instruction = next(instructions, None)
            if not instruction:
                # no more instructions. the last cycle was the actual end. decrement clock and stop
                clock -= 1
                break
            op, *params = instruction.split(" ")

        # monitor *during* cycle
        if (clock - 20) % 40 == 0:
            signal = clock * register_x
            signals.append((clock, signal))
            # print(f"clock: {clock} register_x: {register_x} signal: {signal}")
            total_signal += signal

        # print(f"clock: {clock} register_x: {register_x} op: {op} params: {params}")
        # handle op
        if op == "noop":
            op = None
        elif op == "addx":
            if cycles_left is None:
                cycles_left = 2

            cycles_left -= 1

            if cycles_left == 0:
                register_x += int(params[0])
                op = None
                params = None
                cycles_left = None
        else:
            raise Exception(f"Unknonw instruction: {instruction}")


        # print(f"clock: {clock} register_x: {register_x}")


    return (clock, register_x, total_signal, signals)


def execute_program(state: State, instructions: Iterator[str]) -> tuple[State, int]:
    return functools.reduce(wrapper, instructions, (state, 0))


def wrapper(state_signal: tuple[State, int], instruction: str) -> tuple[State, int]:
    state = handle_instruction(state_signal[0], instruction)
    signal = state_signal[1]
    if (state.clock - 20) % 40 == 0:
        signal += state.clock * state.register_x
    return (state, signal)


def handle_instruction(state: State, instruction: str) -> State:
    opcode, *params = instruction.split(" ")
    if opcode == "addx":
        x = state.register_x + int(params[0])
        clock = state.clock + 2
        return dataclasses.replace(state, clock=clock, register_x=x)
    elif opcode == "noop":
        return dataclasses.replace(state, clock=state.clock + 1)
    else:
        raise Exception(f"Unknown instruction: {instruction}")


def test1a():
    input = ["noop", "addx 3", "addx -5"]
    # state, signal = execute_program(init_state(), iter(input))
    # print(state)
    # assert state.clock == 5
    # assert state.register_x == -1
    (clock, register_x, total_signal, signals) = run_computer(iter(input))
    assert clock == 5, clock
    assert register_x == -1, register_x


def test1b():
    input = utils.read_input("input/day10-part1-test.txt")
    (clock, register_x, total_signal, signals) = run_computer(iter(input))
    print(clock)
    print(register_x)
    print(total_signal)
    assert signals[0][0] == 20
    assert signals[0][1] == 420
    assert signals[1][0] == 60
    assert signals[1][1] == 1140
    assert signals[2][0] == 100
    assert signals[2][1] == 1800
    assert signals[3][0] == 140
    assert signals[3][1] == 2940
    assert signals[4][0] == 180
    assert signals[4][1] == 2880
    assert signals[5][0] == 220
    assert signals[5][1] == 3960, signals[5][1]
    assert sum(signal[1] for signal in signals) == 13140

def part1():
    input = utils.read_input("input/day10-part1.txt")
    (clock, register_x, total_signal, signals) = run_computer(iter(input))
    print(total_signal)
    assert total_signal == 14780

def main():
    test1a()
    test1b()
    part1()
