"""
Write tests for division() function in 2_python_part_2/task_exceptions.py
In case (1,1) it should check if exception were raised
In case (1,0) it should check if return value is None and "Division by 0" printed
If other cases it should check if division is correct

TIP: to test output of print() function use capfd fixture
https://stackoverflow.com/a/20507769
"""

import typing
import pytest

class DivisionByOneException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

def division(x: int, y: int) -> typing.Union[None, int]:
    try:
        if y == 0:
            print("Division by 0")
            return None
        elif y == 1:
            raise DivisionByOneException("Deletion on 1 get the same result")
        else:
            result = x // y  # Integer division
            return result
    except DivisionByOneException as e:
        print(f"{type(e).__name__}(\"{e}\")")
    finally:
        print("Division finished")

def test_division_ok(capfd):
    result = division(1, 2)
    out, err = capfd.readouterr()
    assert result == 0
    assert out == "Division finished\n"
    assert err == ""

    result = division(2, 2)
    out, err = capfd.readouterr()
    assert result == 1
    assert out == "Division finished\n"
    assert err == ""

def test_division_by_zero(capfd):
    result = division(1, 0)
    out, err = capfd.readouterr()
    assert result is None
    assert out == "Division by 0\nDivision finished\n"
    assert err == ""

def test_division_by_one(capfd):
    division(1, 1)
    out, err = capfd.readouterr()
    assert "DivisionByOneException(\"Deletion on 1 get the same result\")" in out
    assert "Division finished" in out
    assert err == ""

if __name__ == "__main__":
    pytest.main(["-v"])