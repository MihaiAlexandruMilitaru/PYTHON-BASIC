# """
# Write function which executes custom operation from math module
# for given arguments.
# Restrition: math function could take 1 or 2 arguments
# If given operation does not exists, raise OperationNotFoundException
# Examples:
#      >>> math_calculate('log', 1024, 2)
#      10.0
#      >>> math_calculate('ceil', 10.7)
#      11
# """
import math


class OperationNotFoundException(Exception):
    def __init__(self):
        self.message = "Operation not found"

class OperationArgumentsException(Exception):
    def __init__(self):
        self.message = "Invalid number of arguments"


def math_calculate(function: str, *args):
    try:
        f = getattr(math, function)
    except AttributeError:
        raise OperationNotFoundException

    try:
        return f(*args)
    except TypeError:
        raise OperationArgumentsException


"""
Write tests for math_calculate function
"""

import pytest


def test_math_calculate():
    assert math_calculate('log', 1024, 2) == 10.0
    assert math_calculate('ceil', 10.7) == 11
    with pytest.raises(OperationNotFoundException):
        math_calculate('log8', 1024, 2)
    with pytest.raises(OperationArgumentsException):
        math_calculate('log2', 10.7, 2)


if __name__ == "__main__":

    test_math_calculate()
    print("math_calculate PASSED")