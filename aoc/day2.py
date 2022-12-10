"""
    A = rock
    B = paper
    C = scissors

    X = rock
    Y = paper
    Z = scissors

     2
     XYZ
  1 A 21 
    B1 2
    C21
"""

from typing import Iterable


def read_rounds(file_name: str) -> Iterable[tuple[str, str]]:
    with open(file_name, "rt") as f:
        for line in f:
            yield tuple(line.strip().split(" "))


def score(round: tuple[str, str]) -> tuple[int, int]:
    if round == ("A", "X"):
        return (1 + 3, 1 + 3)
    elif round == ("A", "Y"):
        return (1 + 0, 2 + 6)
    elif round == ("A", "Z"):
        return (1 + 6, 3 + 0)
    elif round == ("B", "X"):
        return (2 + 6, 1 + 0)
    elif round == ("B", "Y"):
        return (2 + 3, 2 + 3)
    elif round == ("B", "Z"):
        return (2 + 0, 3 + 6)
    elif round == ("C", "X"):
        return (3 + 0, 1 + 6)
    elif round == ("C", "Y"):
        return (3 + 6, 2 + 0)
    elif round == ("C", "Z"):
        return (3 + 3, 3 + 3)


def calc_play(strategy: tuple[str, str]) -> tuple[str, str]:
    """calc play for given strategy.

    X means you need to lose.
    Y means you need to end the round in a draw.
    Z means you need to win.
    """
    if strategy == ("A", "X"):
        return ("A", "Z")
    elif strategy == ("A", "Y"):
        return ("A", "X")
    elif strategy == ("A", "Z"):
        return ("A", "Y")
    elif strategy == ("B", "X"):
        return ("B", "X")
    elif strategy == ("B", "Y"):
        return ("B", "Y")
    elif strategy == ("B", "Z"):
        return ("B", "Z")
    elif strategy == ("C", "X"):
        return ("C", "Y")
    elif strategy == ("C", "Y"):
        return ("C", "Z")
    elif strategy == ("C", "Z"):
        return ("C", "X")


def calc_score(rounds: list[tuple[str, str]]) -> int:
    scores = list(map(score, rounds))
    return sum(score[1] for score in scores)


def test1():
    rounds = [("A", "Y"), ("B", "X"), ("C", "Z")]
    assert calc_score(rounds) == 15


def part1():
    return calc_score(read_rounds("input/day2-part1.txt"))


def calc_score_strategy(strategies: list[tuple[str, str]]):
    rounds = list(map(calc_play, strategies))
    scores = list(map(score, rounds))
    return sum(score[1] for score in scores)


def test2():
    strategies = [("A", "Y"), ("B", "X"), ("C", "Z")]
    assert calc_score_strategy(strategies) == 12


def part2():
    strategies = read_rounds("input/day2-part1.txt")
    rounds = list(map(calc_play, strategies))
    scores = list(map(score, rounds))
    return sum(score[1] for score in scores)


if __name__ == "__main__":
    test1()
    print(part1())
    test2()
    print(part2())
