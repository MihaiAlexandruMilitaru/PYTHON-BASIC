"""
Write tests for a read_numbers function.
It should check successful and failed cases
for example:
Test if user inputs: 1, 2, 3, 4
Test if user inputs: 1, 2, Text

Tip: for passing custom values to the input() function
Use unittest.mock patch function
https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch

TIP: for testing builtin input() function create another function which return input() and mock returned value
"""
from unittest.mock import patch
from task_input_output import read_numbers
import unittest

@patch('task_input_output.input', side_effect=['1', '2', '3', '4'])
def test_read_numbers_test1(mock_input):
    with patch('builtins.print') as mock_print:
        read_numbers(4)
        mock_print.assert_called_with('Avg: 2.50')

@patch('task_input_output.input', side_effect=['1', '2', 'Text'])
def test_read_numbers_test2(mock_input):
    with patch('builtins.print') as mock_print:
        read_numbers(3)
        mock_print.assert_called_with('Avg: 1.50')


@patch('task_input_output.input', side_effect=['abc', 'def', 'ghi'])
def test_read_numbers_test3(mock_input):
    with patch('builtins.print') as mock_print:
        read_numbers(3)
        mock_print.assert_called_with('No numbers entered')


if __name__ == '__main__':
    unittest.main()