import concurrent.futures
import os
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures.process import ProcessPoolExecutor
import time
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

def worker_function(n):
    result = fib(n)
    file_name = f'{OUTPUT_DIR}/{n}.txt'
    with open(file_name, 'w') as file:
        file.write(str(result))


def func1(array: list):

    workers = 8
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        executor.map(worker_function, array)

def worker_function2(file_name):
    n = int(file_name.split('.')[0])
    result = fib(n)
    with open(RESULT_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([n, result])

def func2(result_file: str):
    all_file = os.listdir(OUTPUT_DIR)
    with open(result_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['n', 'fib(n)'])

    workers = 8
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        executor.map(worker_function2, all_file)



if __name__ == '__main__':
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    start = time.time()

    func1(array=[randint(10, 100) for _ in range(10)])
    func2(result_file=RESULT_FILE)

    end = time.time()

    print(f"Execution time: {end - start}")
