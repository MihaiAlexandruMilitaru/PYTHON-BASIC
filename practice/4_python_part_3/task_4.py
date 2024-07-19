"""
Create virtual environment and install Faker package only for this venv.
Write command line tool which will receive int as a first argument and one or more named arguments
 and generates defined number of dicts separated by new line.
Exec format:
`$python task_4.py NUMBER --FIELD=PROVIDER [--FIELD=PROVIDER...]`
where:
NUMBER - positive number of generated instances
FIELD - key used in generated dict
PROVIDER - name of Faker provider
Example:
`$python task_4.py 2 --fake-address=address --some_name=name`
{"some_name": "Chad Baird", "fake-address": "62323 Hobbs Green\nMaryshire, WY 48636"}
{"some_name": "Courtney Duncan", "fake-address": "8107 Nicole Orchard Suite 762\nJosephchester, WI 05981"}
"""

import argparse
import faker
import json
from faker import Faker
import sys

def print_name_address(args: argparse.Namespace) -> None:

    fake = Faker()
    if "--fields" not in args.args:
        raise ValueError("No --fields keyword")
    pairs = args.args[1:]

    for i in range(args.number):
        data = {}
        for pair in pairs:
            field, provider = pair.split("=")
            # check if provider is valid
            if not hasattr(fake, provider):
                raise ValueError("Invalid provider")
            data[field] = getattr(fake, provider)()
        print(json.dumps(data))



# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Generate fake data.")
#     parser.add_argument("number", type=int, help="Number of generated instances")
#
#     # rest of the are unknown named arguments
#     parser.add_argument("args", nargs=argparse.REMAINDER)
#     print_name_address(parser.parse_args())
#
#
# """
# Write test for print_name_address function
# Use Mock for mocking args argument https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
# Example:
#     >>> m = Mock()
#     >>> m.method.return_value = 123
#     >>> m.method()
#     123
# """


import unittest
from unittest.mock import Mock
import sys
from io import StringIO
import json

class TestPrintNameAddress(unittest.TestCase):

    def test_print_name_address(self):
        m = Mock()
        m.number = 2
        m.args = ["--fields", "nume=name", "adresa=address"]

        print_name_address(m)

        m.number = 3
        m.args = ["--fields", "nume=name", "adresa=address", "oras=city"]
        print_name_address(m)

if __name__ == "__main__":
    unittest.main()

