import math
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from timeit import timeit


def integrate(f, a, b, n_iter=1000):
    start_log = (
        time.time(), f"starting integrate function {f.__name__} from {a} to {b}")
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    finish_log = (
        time.time(), f"finished integrate function {f.__name__} from {a} to {b}")
    return ((start_log, finish_log), acc)


def integrate_threads(f, a, b, *, n_jobs=1, n_iter=1000):
    logs.append(
        (time.time(), f"integrating with threads with n_jobs={n_jobs}"))
    res = []
    with ThreadPoolExecutor(max_workers=n_jobs) as executor:
        step = (b - a) / n_jobs
        for i in range(n_jobs):
            res.append(executor.submit(integrate, f, a + i * step,
                       a + (i + 1) * step, n_iter // n_jobs))
    ans = sum([x.result()[1] for x in res])
    for x in res:
        logs.append(x.result()[0][0])
        logs.append(x.result()[0][1])
    return ans


def integrate_processes(f, a, b, *, n_jobs=1, n_iter=1000):
    logs.append(
        (time.time(), f"integrating with threads with n_jobs={n_jobs}"))
    res = []
    with ProcessPoolExecutor(max_workers=n_jobs) as executor:
        step = (b - a) / n_jobs
        for i in range(n_jobs):
            res.append(executor.submit(integrate, f, a + i * step,
                       a + (i + 1) * step, n_iter // n_jobs))
    ans = sum([x.result()[1] for x in res])
    for x in res:
        logs.append(x.result()[0][0])
        logs.append(x.result()[0][1])
    return ans


logs = []


def get_time_threads(n_jobs):
    global logs
    logs = []
    return timeit(lambda: integrate_threads(math.cos, 0, math.pi / 2, n_jobs=n_jobs, n_iter=2*10 ** 7), number=1)


def get_time_processes(n_jobs):
    global logs
    logs = []
    return timeit(lambda: integrate_processes(math.cos, 0, math.pi / 2, n_jobs=n_jobs, n_iter=2*10 ** 7), number=1)


def print_logs_threads():
    with open("artifacts/medium-logs-threads.txt", "w") as logfile, \
            open("artifacts/medium-time-threads.txt", "w") as timefile:
        for i in range(1, 33):
            time = get_time_threads(i)
            print(f"n_jobs = {i}, time is: {time}", file=timefile)
            for log in sorted(logs):
                print(log[1], file=logfile)
            print("-" * 100, file=logfile)


def print_logs_processes():
    with open("artifacts/medium-logs-processes.txt", "w") as logfile, \
            open("artifacts/medium-time-processes.txt", "w") as timefile:
        for i in range(1, 17):
            time = get_time_processes(i)
            print(f"n_jobs = {i}, time is: {time}", file=timefile)
            for log in sorted(logs):
                print(log[1], file=logfile)
            print("-" * 100, file=logfile)


print_logs_threads()
print_logs_processes()
