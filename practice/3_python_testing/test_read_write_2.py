"""
Write tests for 2_python_part_2/task_read_write_2.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""
"""
Example:
    Input: ['abc', 'def', 'xyz']

    Output:
        file1.txt (content: "abc\ndef\nxyz", encoding: UTF-8)
        file2.txt (content: "xyz,def,abc", encoding: CP1252)
"""

import os
import re
from typing import List
from tempfile import NamedTemporaryFile
from task_read_write_2 import task_read_write_2
def test_task_read_write_2():

    # create a temprary utf-8 file

    with NamedTemporaryFile(mode='w', encoding='utf-8') as f1:
        f1_path = f1.name

    # create a temprary cp1252 file

    with NamedTemporaryFile(mode='w', encoding='cp1252') as f2:
        f2_path = f2.name

    # call the function task_read_write_2
    task_read_write_2(f1_path, f2_path)

    # Check if the result file was created

    assert os.path.exists(f1_path), 'Result file with encoding UTF-8 was not created'

    assert os.path.exists(f2_path), 'Result file with encoding CP1252 was not created'

    words = task_read_write_2(f1_path, f2_path)

    # Check if the content of the files is correct

    with open(f1_path, 'r', encoding='utf-8') as f1:
        content = f1.read()
        assert content == '\n'.join(words), 'Content of the file with encoding UTF-8 is not correct'

    with open(f2_path, 'r', encoding='cp1252') as f2:
        content = f2.read()
        assert content == ','.join(reversed(words)), 'Content of the file with encoding CP1252 is not correct'



if __name__ == '__main__':
    test_task_read_write_2()
    print('All tests passed')