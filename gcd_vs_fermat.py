import time
import math


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
def gcd(n):
    """İşlemleri doğrudan yapan fonksiyon."""
    total = 0
    for i in range(n):
        a = math.gcd(i, n)
    return total


@cpu_time_decorator
def fermat(n):
    """Fonksiyon çağrılarıyla aynı işlemleri yapan fonksiyon."""
    total = 0
    for i in range(n):
        a = pow(i, n - 1, n)
    return total


n = 10**7

# İşlemleri doğrudan yapan fonksiyon
gcd(n)

# İşlemleri fonksiyon çağrılarıyla yapan fonksiyon
fermat(n)
