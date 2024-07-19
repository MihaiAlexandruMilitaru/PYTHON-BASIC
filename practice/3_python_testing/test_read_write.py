"""
Write tests for 2_python_part_2/task_read_write.py task.
To write files during tests use temporary files:
https://docs.python.org/3/library/tempfile.html
https://docs.pytest.org/en/6.2.x/tmpdir.html
"""

import os
import re
from typing import List
from tempfile import NamedTemporaryFile

from task_read_write import read_write

#

def test_task_read_write():

    current_path = os.getcwd()

    with NamedTemporaryFile(mode='w', delete=False, dir=current_path, suffix=".txt", prefix='1-') as f1:
        f1.write('23')
        f1_path = f1.name

    with NamedTemporaryFile(mode='w', delete=False, dir=current_path, suffix=".txt", prefix='2-') as f2:
        f2.write('78')
        f2_path = f2.name

    with NamedTemporaryFile(mode='w', delete=False, dir=current_path, suffix=".txt", prefix='3-') as f3:
        f3.write('3')
        f3_path = f3.name

    output_filename = 'result.txt'

    read_write(current_path, output_filename)

    # delete temporary files

    os.remove(f1_path)
    os.remove(f2_path)
    os.remove(f3_path)

    # Check if the result file was created

    assert os.path.exists(f'{current_path}/{output_filename}'), 'Result file was not created'

    # Check if the result file has the correct content

    with open(f'{current_path}/{output_filename}', 'r') as f:
        assert f.read().strip() == '23, 78, 3', 'Values are not correct'

if __name__ == '__main__':
    test_task_read_write()
    print('All tests passed')


