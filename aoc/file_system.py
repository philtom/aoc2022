import dataclasses
from typing import Iterator, Optional
import functools

@dataclasses.dataclass
class File:
    name: str
    size: int

@dataclasses.dataclass
class Directory:
    name: str
    parent: Optional["Directory"]
    directories: list["Directory"] = dataclasses.field(default_factory=list)
    files: list[File] = dataclasses.field(default_factory=list)

def create_new_file_system():
    return Directory(name="/", parent=None)

def make_directory(current_directory: Directory, name: str) -> Directory:
    directory = Directory(name=name, parent=current_directory)
    current_directory.directories.append(directory)
    return current_directory

def add_file(current_directory: Directory, name: str, size: int) -> Directory:
    file = File(name=name, size=size)
    current_directory.files.append(file)
    return current_directory

def change_directory(current_directory: Directory, name: str) -> Directory:
    if name == "/":
        directory = current_directory
        while directory.parent is not None:
            directory = directory.parent
        return directory
    elif name == "..":
        return current_directory.parent

    return [directory for directory in current_directory.directories if directory.name == name][0]

def calc_total_size(current_directory: Directory) -> int:
    current_directory_size = sum(file.size for file in current_directory.files)
    return current_directory_size + sum(map(calc_total_size, current_directory.directories))

def calc_total_size_with_max_dir_size(max_dir_size: int, current_directory: Directory) -> int:
    total_size = calc_total_size(current_directory)
    print(f"{current_directory.name} {total_size}")
    if total_size <= max_dir_size:
        return total_size
    if len(current_directory.directories) == 0:
        return 0
    _calc_total_size_with_max_dir_size = functools.partial(calc_total_size_with_max_dir_size, max_dir_size)
    return sum(map(_calc_total_size_with_max_dir_size, current_directory.directories))

def find_directories(current_directory: Directory) -> Iterator[Directory]:
    return _find_directories_acc([], current_directory)

def _find_directories_acc(accumulated_directories: list[Directory], current_directory: Directory) -> list[Directory]:
    if len(current_directory.directories) == 0:
        return accumulated_directories + [current_directory]
    fn = functools.partial(_find_directories_acc, accumulated_directories)
    return _flatten(map(fn, current_directory.directories)) + [current_directory]

def _flatten(it):
    return [e for l in it for e in l]