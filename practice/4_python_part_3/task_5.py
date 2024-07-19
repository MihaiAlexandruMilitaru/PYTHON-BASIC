# """
# Write a function that makes a request to some url
# using urllib. Return status code and decoded response data in utf-8
# Examples:
#      >>> make_request('https://www.google.com')
#      200, 'response data'
# """
from typing import Tuple
import urllib.request
import sys

def make_request(url: str) -> Tuple[int, str]:
    try:
        response = urllib.request.urlopen(url)
        return response.code, response.read().decode('utf-8')
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)



"""
Write test for make_request function
Use Mock for mocking request with urlopen https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 200
    >>> m.method2.return_value = b'some text'
    >>> m.method()
    200
    >>> m.method2()
    b'some text'
"""

import unittest
from unittest.mock import Mock, patch


def test_make_request():
    m = Mock()
    m.code = 200
    m.read.return_value = b'response body'
    with patch('urllib.request.urlopen', return_value=m):
        code, data = make_request('https://www.google.com')
        assert code == 200
        assert len(data)


if __name__ == '__main__':

    test_make_request()
    print('All tests passed')

