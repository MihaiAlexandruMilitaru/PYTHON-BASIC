"""
Write a parametrized test for two functions.
The functions are used to find a number by ordinal in the Fibonacci sequence.
One of them has a bug.

Fibonacci sequence: https://en.wikipedia.org/wiki/Fibonacci_number

Task:
 1. Write a test with @pytest.mark.parametrize decorator.
 2. Find the buggy function and fix it.
"""

import pytest

def fibonacci_1(n):
    a, b = 0, 1
    for _ in range(n-1):
        a, b = b, a + b
    return a


def fibonacci_2(n):
    if n == 1:
        return 0
    elif n == 2:
        return 1
    fibo = [0, 1]
    for i in range(2, n):
        fibo.append(fibo[i-1] + fibo[i-2])
    return fibo[-1]

@pytest.mark.parametrize("n, expected", [
    (1, 0),
    (2, 1),
    (3, 1),
    (4, 2),
    (5, 3),
    (6, 5),
    (7, 8),
    (8, 13),
    (9, 21),
    (10, 34)
])
def test_fibonacci_1(n, expected):
    assert fibonacci_1(n) == expected


@pytest.mark.parametrize("n, expected", [
    (1, 0),
    (2, 1),
    (3, 1),
    (4, 2),
    (5, 3),
    (6, 5),
    (7, 8),
    (8, 13),
    (9, 21),
    (10, 34)
])
def test_fibonacci_2(n, expected):
    assert fibonacci_2(n) == expected


if __name__ == '__main__':
    pytest.main()