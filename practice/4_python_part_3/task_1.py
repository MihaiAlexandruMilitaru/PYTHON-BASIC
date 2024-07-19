# """
# using datetime module find number of days from custom date to now
# Custom date is a string with format "2021-12-24"
# If entered string pattern does not match, raise a custom Exception
# If entered date is from future, return negative value for number of days
#     >>> calculate_days('2021-10-07')  # for this example today is 6 october 2021
#     -1
#     >>> calculate_days('2021-10-05')
#     1
#     >>> calculate_days('10-07-2021')
#     WrongFormatException
# """
from datetime import datetime
import pytest
from freezegun import freeze_time

class WrongFormatException(Exception):
    def __init__(self):
        self.message = "WrongFormatException"

@freeze_time("2021-10-06")

def calculate_days(from_date: str) -> int:
    try:

        date = datetime.strptime(from_date, "%Y-%m-%d")
        delta = datetime.now() - date
        return delta.days
    except ValueError:
        raise WrongFormatException


"""
Write tests for calculate_days function
Note that all tests should pass regardless of the day test was run
Tip: for mocking datetime.now() use https://pypi.org/project/pytest-freezegun/
"""

def test_calculate_days():
    assert calculate_days('2021-10-07') == -1
    assert calculate_days('2021-10-05') == 1
    with pytest.raises(WrongFormatException):
        calculate_days('10-07-2021')



