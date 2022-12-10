from typing import Iterator


def read_input(file_name: str) -> Iterator[str]:
    """Generator for lines in a file.

    Removes the new-line if it exists
    """
    with open(file_name, "rt") as f:
        for line in f:
            if line[-1] == "\n":
                yield line[:-1]
            else:
                yield line
