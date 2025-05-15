import numpy as np
import sys

# NumPy boolean array
limit = 100
is_prime = np.ones(limit + 1, dtype=bool)  # Bellek açısından verimli boolean dizisi
is_prime[0:2] = False  # 0 ve 1 asal değil
print(sys.getsizeof(is_prime[0]), sys.getsizeof(is_prime[-1]))

from bitarray import bitarray

# Standart Python listesi
is_prime_list = [True] * 1000  # Bu, her eleman için 1 byte veya daha fazla yer kaplar.

# Bitarray kullanımı
is_prime_bitarray = bitarray(1000)  # Bu ise her eleman için sadece 1 bit yer kaplar.
is_prime_bitarray.setall(True)
print(sys.getsizeof(is_prime_list[0]), sys.getsizeof(is_prime_list[-1]))


a = [True, False] * 1000
print(sys.getsizeof(a[0]), sys.getsizeof(a[-1]))