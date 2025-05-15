import random
import numpy as np
import time

n = 1_000_000  # 1 milyon sayı üretelim

# random.randint() ile
start = time.time()
for _ in range(n):
    a = random.randint(2, 1000)
end = time.time()
print(f"random.randint() ile süre: {end - start:.5f} saniye")

# numpy.random.randint() ile
start = time.time()
for _ in range(n):
    a = np.random.randint(2, 1000, size=1)  # Tek seferde 1 milyon sayı üret
end = time.time()
print(f"numpy.random.randint(size=1) ile süre: {end - start:.5f} saniye")

start = time.time()
a = np.random.randint(2, 1000, size=n)  # Tek seferde 1 milyon sayı üret
print(type(a))
end = time.time()
print(f"numpy.random.randint(size={n}) ile süre: {end - start:.5f} saniye")

start = time.time()
for _ in range(n):
    a = np.random.randint(2, 1000)  # Tek seferde 1 milyon sayı üret
end = time.time()
print(f"numpy.random.randint() ile süre: {end - start:.5f} saniye")
