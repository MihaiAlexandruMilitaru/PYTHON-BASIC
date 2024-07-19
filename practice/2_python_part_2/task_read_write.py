"""
Read files from ./files and extract values from them.
Write one file with all values separated by commas.

Example:
    Input:

    file_1.txt (content: "23")
    file_2.txt (content: "78")
    file_3.txt (content: "3")

    Output:

    result.txt(content: "23, 78, 3")
"""

import os
from typing import List
import re

def read_write(file_path, output_filename) -> None:

    def sort_key(file_name):
        match = re.search(r'\d+', file_name)
        return int(match.group()) if match else 0

    # Get and sort the file names using the custom key, and filter for .txt files
    files = [file for file in os.listdir(file_path) if file.endswith('.txt')]
    sorted_files = sorted(files, key=sort_key)

    values = []

    for file in sorted_files:
        with open(f'{file_path}/{file}', 'r') as f:
            values.append(f.read().strip())

    with open(f'{file_path}/{output_filename}', 'w') as f:
        f.write(', '.join(values))


if __name__ == '__main__':
    file_path = './files'
    output_filename = 'result.txt'
    read_write(file_path, output_filename)
    print('All tests passed')

