import numpy as np
import time
import math

n = 2**63#2**24
a = []

start_real = time.time()
start_cpu = time.process_time()
start_wall = time.perf_counter()
for _ in range(n, n + 2**10):
    a.append(np.int64(np.sqrt(_)))
end_real = time.time()
end_cpu = time.process_time()
end_wall = time.perf_counter()
print(f"np.int64(np.sqrt(n)) ile real: {end_real - start_real:.5f} saniye")
print(f"np.int64(np.sqrt(n)) ile cpu: {end_cpu - start_cpu:.5f} saniye")
print(f"np.int64(np.sqrt(n)) ile wall: {end_wall - start_wall:.5f} saniye\n")

start_real = time.time()
start_cpu = time.process_time()
start_wall = time.perf_counter()
for _ in range(n, n + 2 ** 10):
    a.append(math.isqrt(_))
end_real = time.time()
end_cpu = time.process_time()
end_wall = time.perf_counter()
print(f"math.isqrt(n) ile real: {end_real - start_real:.5f} saniye")
print(f"math.isqrt(n) ile cpu: {end_cpu - start_cpu:.5f} saniye")
print(f"math.isqrt(n) ile wall: {end_wall - start_wall:.5f} saniye")