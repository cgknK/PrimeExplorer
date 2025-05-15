import math
#from functools import lru_cache
import numpy as np
from scipy.special import factorial as f
import time
import decimal


def cpu_time_decorator(func):
    def wrapper(*args, **kwargs):
        start_cpu_time = time.process_time()
        start_wall_time = time.perf_counter()
        start_wall_time_ns = time.perf_counter_ns()
        
        result = func(*args, **kwargs)

        end_wall_time = time.perf_counter()
        end_wall_time_ns = time.perf_counter_ns()
        end_cpu_time = time.process_time()
        cpu_time_used = end_cpu_time - start_cpu_time
        wall_time = end_wall_time - start_wall_time
        wall_time_ns = end_wall_time_ns - start_wall_time_ns
        wall_time_ms = wall_time_ns / 1_000_000
        print(f"CPU time used by {func.__name__}: {cpu_time_used:.6f} or {cpu_time_used} seconds")
        print(f"wall_time by {func.__name__}: {wall_time} seconds")
        print(f"wall_time ms by {func.__name__}: {wall_time_ms} ms\n")
        
        return result
    return wrapper


@cpu_time_decorator
def calculate_e_taylor_series_numpy(precision=10):
    n = np.arange(precision, dtype=np.int64)
    factorials = np.vectorize(math.factorial)(n)
    terms = 1 / factorials
    return np.sum(terms)

@cpu_time_decorator
def calculate_e_taylor_series_numpy_and_scipy(precision=10):
    n = np.arange(precision, dtype=np.int64)
    factorials = f(n, exact=True)
    terms = 1 / factorials
    return np.sum(terms)


@cpu_time_decorator
def calculate_e_taylor_series(precision=10):
    e_value = 0
    for n in range(precision):
        e_value += 1 / math.factorial(n)
    return e_value


@cpu_time_decorator
def calculate_e_limit(limit=1000000):
    return (1 + 1/limit) ** limit


@cpu_time_decorator
def calculate_e_limit_decimal(limit=1000000):
    with decimal.localcontext() as ctx:
        ctx.prec = 100  # Hassasiyeti artırmak için
        limit = decimal.Decimal(limit)
        e_value = (1 + 1/limit) ** limit
    return e_value


#result = calculate_e_taylor_series_numpy(10_000)
result_numpy_scipy = calculate_e_taylor_series_numpy_and_scipy(10_000)
result_taylor_series = calculate_e_taylor_series(10_000)
result_limit = calculate_e_limit(10 ** 15)
result_limit_decimal = calculate_e_limit_decimal(10 ** 50)
result_math = math.e

print(result_taylor_series)
print(result_limit)
print(result_math)
print(result_limit_decimal)

print(math.isclose(result_numpy_scipy, result_math))
print(math.isclose(result_taylor_series, result_limit))
print(math.isclose(result_taylor_series, result_math))
print(math.isclose(result_limit, result_math))
print(math.isclose(result_limit_decimal, result_math))