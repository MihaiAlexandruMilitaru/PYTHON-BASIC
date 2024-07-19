"""
Write function which receives filename and reads file line by line and returns min and mix integer from file.
Restriction: filename always valid, each line of file contains valid integer value
Examples:
    # file contains following lines:
        10
        -2
        0
        34
    >>> get_min_max('filename')
    (-2, 34)

Hint:
To read file line-by-line you can use this:
with open(filename) as opened_file:
    for line in opened_file:
        ...
"""
from typing import Tuple


def get_min_max(filename: str) -> Tuple[int, int]:
    min_value = None
    max_value = None
    with open('./files/filename') as opened_file:
        for line in opened_file:
            value = int(line)
            if min_value is None or value < min_value:
                min_value = value
            if max_value is None or value > max_value:
                max_value = value

    return min_value, max_value

