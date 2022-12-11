def find_start_of_message(input: str, code_length: int) -> int:
    for i in range(0, len(input) - code_length):
        if len(set(input[i : i + code_length])) == code_length:
            return i + code_length
    return -1


def test1():
    assert find_start_of_message("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 4) == 7
    assert find_start_of_message("bvwbjplbgvbhsrlpgdmjqwftvncz", 4) == 5
    assert find_start_of_message("nppdvjthqldpwncqszvftbrmjlhg", 4) == 6
    assert find_start_of_message("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4) == 10
    assert find_start_of_message("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4) == 11


def part1():
    with open("input/day6-part1.txt") as f:
        return find_start_of_message(f.readline(), 4)


def test2():
    assert find_start_of_message("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14) == 19
    assert find_start_of_message("bvwbjplbgvbhsrlpgdmjqwftvncz", 14) == 23
    assert find_start_of_message("nppdvjthqldpwncqszvftbrmjlhg", 14) == 23
    assert find_start_of_message("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14) == 29
    assert find_start_of_message("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14) == 26


def part2():
    with open("input/day6-part1.txt") as f:
        return find_start_of_message(f.readline(), 14)


def main():
    test1()
    print(part1())
    test2()
    print(part2())
