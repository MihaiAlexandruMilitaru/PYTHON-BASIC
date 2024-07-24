import os
from random import randint
import csv
import threading
import sys


OUTPUT_DIR = './output'
RESULT_FILE = './output/result.csv'

# Increase the limit for integer string conversion
sys.set_int_max_str_digits(10**6)

def fib(n: int):
    """Calculate a value in the Fibonacci sequence by ordinal number"""

    f0, f1 = 0, 1
    for _ in range(n-1):
        f0, f1 = f1, f0 + f1
    return f1


def func1(array: list):
    numbers = []
    threads = []

    def thread_func(n):
        result = fib(n)
        numbers.append((n, result))

    for n in array:
        thread = threading.Thread(target=thread_func, args=(n,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    numbers.sort(key=lambda x: x[0])

    for nr in numbers:
        file_name = f'{OUTPUT_DIR}/{nr[0]}.txt'
        with open(file_name, 'w') as file:
            file.write(str(nr[1]))


def func2(result_file: str):

    def thread_func(n, result):
        with open(result_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([n, result])

    with open(result_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Input', 'Result'])

    threads = []

    # Read files from the output directory
    for file_name in os.listdir(OUTPUT_DIR):
        with open(f'{OUTPUT_DIR}/{file_name}', 'r') as file:
            try:
                n = int(file_name.split('.')[0])
            except ValueError:
                continue
            result = int(file.read())
            thread = threading.Thread(target=thread_func, args=(n, result))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()



if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    func1(array=[randint(10, 100) for _ in range(10)])
    func2(result_file=RESULT_FILE)
