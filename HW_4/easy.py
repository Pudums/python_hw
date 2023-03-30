from multiprocessing import Pool, Process
from timeit import timeit
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def fib(n: int):
    if n < 1:
        return 0
    a = 0
    b = 1
    while n > 0:
        a, b = b, a + b
        n -= 1
    return b


def threads_time(n_jobs=1, num=10 ** 6, count=100):
    with ThreadPoolExecutor(n_jobs) as executor:
        return executor.map(fib, [num for i in range(count)])


def process_time(n_jobs=1, num=10 ** 6, count=100):
    with ProcessPoolExecutor(n_jobs) as executor:
        return executor.map(fib, [num for i in range(count)])


def non_parallel(count=100, num=10 * 6):
    ans = []
    for i in range(count):
        ans.append(fib(num))
    return ans


def print_all(fout, count, num, n_jobs):
    print(f"non parallel, {count} fibonacci numbers {num}: " + str(
        timeit(lambda: non_parallel(count, num), number=1)) + "s", file=fout)
    print(f"{n_jobs} threads , {count} fibonacci numbers {num}: " + str(
        timeit(lambda: threads_time(n_jobs, num, count), number=1)) + "s", file=fout)
    print(f"{n_jobs} processes, {count} fibonacci numbers {num}: " + str(
        timeit(lambda: process_time(n_jobs, num, count), number=1)) + "s", file=fout)


with open("artifacts/easy.txt", "w") as fout:
    print_all(fout, 100, 10 ** 5, 16)
