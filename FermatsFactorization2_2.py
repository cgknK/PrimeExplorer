import math
from bitarray import bitarray
from concurrent.futures import ProcessPoolExecutor
import random
import time
import logging

# Logging yapılandırması
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def optimized_sieve_of_eratosthenes(limit: int) -> list[int]:
    """Optimize edilmiş Eratosthenes'in Eleği algoritması ile asal sayıları bulur.

    Args:
        limit (int): Asal sayıların bulunacağı üst sınır.

    Returns:
        list[int]: Bulunan asal sayıların listesi.
    """
    if limit < 2:
        return []

    is_prime = bitarray(limit + 1)
    is_prime.setall(False)
    
    # 2 ve tek sayılar için işleme başla
    is_prime[2] = True
    for num in range(3, limit + 1, 2):
        is_prime[num] = True

    # Eleme işlemi optimize edildi, sadece tek sayılar üzerinden gidiyoruz
    for num in range(3, int(math.sqrt(limit)) + 1, 2):
        if is_prime[num]:
            for multiple in range(num * num, limit + 1, num * 2):
                is_prime[multiple] = False

    return [2] + [num for num in range(3, limit + 1, 2) if is_prime[num]]

def random_prime_pair_choice(primes: list[int]) -> tuple[int, int]:
    """İki asal sayı seçmek için random.sample kullanır."""
    return random.sample(primes, 2)

# Memoization kullanarak kare kontrolü
square_cache = {}

def is_square(n: int) -> bool:
    """Bir sayının tam kare olup olmadığını memoization ile kontrol eder."""
    if n in square_cache:
        return square_cache[n]
    sqrt_n = int(math.isqrt(n))
    result = sqrt_n * sqrt_n == n
    square_cache[n] = result
    return result

def fermat_factorization(num: int, max_iterations: int = 10**8) -> tuple[int, int, int]:
    """Fermat faktorizasyonu.

    Args:
        num (int): Faktörleri bulunacak sayı.
        max_iterations (int): Maksimum iterasyon sayısı.

    Returns:
        tuple[int, int, int]: Bulunan çarpanlar veya None, iterasyon sayısı.
    """
    a = int(math.isqrt(num)) + 1
    delta = a * a - num
    
    for i in range(max_iterations):
        if is_square(delta):
            b = int(math.isqrt(delta))
            return a - b, a + b, i
        a += 1
        delta = a * a - num

    return None, max_iterations

def fermat_factorization_limited(num: int, time_limit: int = 15) -> tuple[int, int, int]:
    """Fermat faktorizasyonu, zaman sınırı ile.

    Args:
        num (int): Faktörleri bulunacak sayı.
        time_limit (int): Maksimum süre (saniye).

    Returns:
        tuple[int, int, int]: Bulunan çarpanlar veya None.
    """
    a = int(math.isqrt(num)) + 1
    delta = a * a - num
    count = 0
    start_time = time.process_time()

    while not is_square(delta):
        if time.process_time() - start_time > time_limit:
            return None, count
        a += 1
        delta = a * a - num
        count += 1

    b = int(math.isqrt(delta))
    return a - b, a + b, count

def check_result(n: int, factors: tuple[int, int, int]) -> bool:
    """Çarpanların doğruluğunu kontrol eder."""
    if factors is None or None in factors:
        return False
    p, q = factors[:2]
    return p * q == n

def run_fermat_factorizations(primes: list[int], num_tests: int = 25):
    """Fermat faktorizasyonu ve zaman sınırlı faktorizasyonu test eder."""
    fermat_success = fermat_failure = 0
    llm_success = llm_failure = 0

    for _ in range(num_tests):
        p, q = random_prime_pair_choice(primes)
        n = p * q

        result_fermats = fermat_factorization(n)
        result_llm = fermat_factorization_limited(n)

        if check_result(n, result_fermats):
            fermat_success += 1
        else:
            fermat_failure += 1
            logging.warning(f"Fermat faktorizasyonu başarısız: {result_fermats}, doğru çarpanlar: {p}, {q}")
        
        if check_result(n, result_llm):
            llm_success += 1
        else:
            llm_failure += 1
            logging.warning(f"Zaman sınırlı Fermat faktorizasyonu başarısız: {result_llm}, doğru çarpanlar: {p}, {q}")

    total_fermat = fermat_success + fermat_failure
    total_llm = llm_success + llm_failure

    fermat_failure_rate = (fermat_failure / total_fermat) * 100 if total_fermat > 0 else 0
    llm_failure_rate = (llm_failure / total_llm) * 100 if total_llm > 0 else 0

    logging.info(f"Fermat faktorizasyonu başarısızlık oranı: {fermat_failure_rate:.2f}%")
    logging.info(f"Zaman sınırlı Fermat faktorizasyonu başarısızlık oranı: {llm_failure_rate:.2f}%")

def parallel_fermat_factorizations(primes: list[int], num_tests: int = 25):
    """Paralel çalışan Fermat faktorizasyonu."""
    with ProcessPoolExecutor() as executor:
        results = executor.map(run_fermat_factorizations, [primes] * num_tests)
    return list(results)

def main():
    primes = optimized_sieve_of_eratosthenes(10**8)
    run_fermat_factorizations(primes)

if __name__ == '__main__':
    main()
