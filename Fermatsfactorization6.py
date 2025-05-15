import math
import numpy as np
import random
import time
from typing import List, Tuple, Optional
from concurrent.futures import ProcessPoolExecutor
import matplotlib.pyplot as plt
import multiprocessing
import cProfile
import os


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


# Asal sayı bulmak için Eratosthenes eleği algoritması
def optimized_sieve_of_eratosthenes_numpy(limit: int) -> List[int]:
    if limit < 2:
        return []

    is_prime = np.zeros(limit + 1, dtype=bool)
    is_prime[2] = True
    is_prime[3:limit + 1:2] = True  # Tüm tek sayılar asal varsayılır

    for num in range(3, int(math.sqrt(limit)) + 1, 2):
        if is_prime[num]:
            is_prime[num * num:limit + 1:num * 2] = False  # Katları asal değil olarak işaretle

    return np.nonzero(is_prime)[0].tolist()  # Asal sayıların listesini döndür


# Rastgele iki asal sayı seçimi
#def random_prime_pair_choice(primes: List[int]) -> Tuple[int, int]:
#    return tuple(random.sample(primes, 2))
def random_prime_pair_choice(primes: List[int]) -> Tuple[int, int]:
    indices = np.random.choice(len(primes), 2, replace=False)
    return primes[indices[0]], primes[indices[1]]



# Bir sayının tam kare olup olmadığını kontrol eden fonksiyon
def is_square(n: int) -> bool:
    sqrt_n = math.isqrt(n)
    return sqrt_n * sqrt_n == n


# Fermat faktorizasyonu #n+b^2=a^2 ile ters yöne sadece None dönenler için bakıp araştır.
def fermat_factorization(num: int, p: int, q: int, time_limit: Optional[int] = None, max_iterations: int = 10**9) -> Tuple[Optional[int], Optional[int], int]:
    a = np.int64(np.ceil(np.sqrt(num)))
    delta = a * a - num
    count = 0
    start_time = time.process_time()

    pid = os.getpid()
    for _ in range(max_iterations):
        if is_square(delta):
            b = np.int64(np.sqrt(delta))
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"Process {pid} ->", a - b, a + b, count, num, p, q, timestamp)
            return [a - b, a + b, count, num, p, q]

        a += 1
        delta = a * a - num
        count += 1

        if time_limit and (time.process_time() - start_time > time_limit):
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"Process {pid} ->", None, None, count, num, p, q, timestamp, f"max_time{time_limit}")
            return [None, None, count, num, p, q]

    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"Process {pid} ->", None, None, count, num, p, q, timestamp, "max_iterations")
    return [None, None, max_iterations, num, p, q]


# Faktorizasyon sonucunu kontrol etme
def check_result(n: int, factors: Tuple[Optional[int], Optional[int], int]) -> bool:
    if factors[0] is None or factors[1] is None:
        return False
    p, q = factors[:2]
    return p * q == n


# Tek bir testi çalıştırma
def run_single_test(primes: List[int], time_limit: Optional[int]) -> bool:
    p, q = random_prime_pair_choice(primes)
    n = p * q
    result_fermats = fermat_factorization(n, p, q, time_limit=time_limit)
    return check_result(n, result_fermats), result_fermats


# Test wrapper fonksiyonu
def run_test_wrapper(args):
    return run_single_test(*args)


# Testleri paralel olarak çalıştırma
def run_tests(primes: List[int], num_tests: int, time_limit: Optional[int], num_workers: int = None) -> List[float]:
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        args = [(primes, time_limit) for _ in range(num_tests)]
        #results = list(executor.map(run_test_wrapper, args, chunksize=1000))
        results = list(executor.map(run_test_wrapper, args))
    
    # `None` sonuçları filtreleme
    valid_results = [result for result in results if result[1][0] is not None and result[1][1] is not None]

    #results sum için düzeltilmeli veya başka birşey sorun burada başlıyor
    successes = len(valid_results)#sum(result[0] for result in valid_results)
    success_rate = (successes / len(results)) * 100 if valid_results else 0
    return success_rate, results


# Başarı oranını zaman limitine göre grafiğe dökme
def plot_success_rate_by_time(primes: List[int], num_tests: int, num_workers: int):
    time_limits = [1, 5, 10, 15, 30]
    #time_limits = [25]
    avg_success_rates = []
    total_results = []
    for time_limit in time_limits:
        success_rate, results = run_tests(primes, num_tests, time_limit, num_workers=num_workers)
        avg_success_rates.append(success_rate)
        total_results += results

    print("avg_success_rates", avg_success_rates)
    # Grafiği çizdir
    plt.figure(figsize=(8, 6))
    plt.plot(time_limits, avg_success_rates, marker='o', linestyle='-', color='b', label='Success Rate')
    plt.title('Success Rate of Fermat Factorization vs. Time Limits')
    plt.xlabel('Time Limit (seconds)')
    plt.ylabel('Average Success Rate (%)')
    plt.grid(True)
    plt.legend()
    plt.show()
    plt.close()

    return total_results


def fermat_reverse_factorization(*args, **kwargs):
    #a^2=n+b^2 && b^2 < n
    data = args[0][1]
    num, p, q = data[3:]
    
    assert num == p * q, "Hata: num, p * q'ya eşit değil."

    b = math.isqrt(num)
    while True:
        sigma = num + b ** 2

        sigma_sqrt = math.isqrt(sigma)
        if sigma_sqrt**2 == sigma:
            fact1 = sigma_sqrt - b
            fact2 = sigma_sqrt + b

            if fact1 * fact2 == num:
                print("Dogru bulundu", fact1, fact2)
                return
            else:
                print("Yanlis bulundu", fact1, fact2)

        b -= 1
        if b == 0:
            break

    print("Bulunamadi", b)


def main():
    limit = 2**26#2**24 
    primes = optimized_sieve_of_eratosthenes_numpy(limit)
    num_tests = 16
    carpan = 1
    num_workers = int(multiprocessing.cpu_count() * carpan) # Farklı çarpanları dene.

    # Başarı oranını zamana göre grafikte göster
    results = plot_success_rate_by_time(primes, num_tests, num_workers)
    for e in results:
        print("\t", e)

    false_results = [result for result in results if not result[0]]

    print(len(false_results), len(results))
    print(len(false_results) / len(results))

    print("\n" * 2, " -> ")
    for false_result in false_results:
        print(false_result)
        fermat_reverse_factorization(false_result)
        print()



    """
    #plot_success_rate_by_time(primes, 3, 4)
    num_workers = [5, 4]
    times = 1

    for e in num_workers:
        cpu_time = 0
        wall_time = 0
        for _ in range(times):
            start_cpu_time = time.process_time()
            start_wall_time = time.perf_counter()
            plot_success_rate_by_time(primes, num_tests, e)
            end_wall_time = time.perf_counter()
            end_cpu_time = time.process_time()
            cpu_time += end_cpu_time - start_cpu_time
            wall_time += end_wall_time - start_wall_time
            print(f"\t{e} -> {_} : cpu:{end_cpu_time - start_cpu_time} , wall:{end_wall_time - start_wall_time}")

        print(f"Worker:{e} , {cpu_time / times}  ,  {wall_time / times}\n")
    """


if __name__ == '__main__':
    main()
    #cProfile.run('main()', 'Fermatsfactorization6_output.stats')
