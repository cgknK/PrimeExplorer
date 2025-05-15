import math
from bitarray import bitarray
import random
import time

def optimized_sieve_of_eratosthenes(limit):
    """Eratosthenes'in Eleği algoritmasının optimize edilmiş versiyonu ile 2'den limit'e kadar olan asal sayıları bulur.

    Args:
        limit (int): Asal sayıların bulunacağı üst sınır.

    Returns:
        list: Bulunan asal sayıların listesi.
    """
    if limit < 2:
        return []

    # Bitarray kullanarak bellek verimliliği sağlıyoruz
    is_prime = bitarray(limit + 1)
    is_prime.setall(False)
    
    # 2'yi ve tek sayıları işleme alacağız
    is_prime[2] = True
    
    for num in range(3, limit + 1, 2):
        is_prime[num] = True

    # 3'ten başlayarak, yalnızca tek sayılar üzerinden eleme yapıyoruz
    for num in range(3, int(math.sqrt(limit)) + 1, 2):
        if is_prime[num]:
            # num'in katlarını işaretlerken çift sayıları atlıyoruz
            for multiple in range(num * num, limit + 1, num * 2):
                is_prime[multiple] = False

    # Asal sayılar listesi döndürülür
    return [2] + [num for num in range(3, limit + 1, 2) if is_prime[num]]


def random_prime_pair_choice(primes):
    """İki asal sayı çifti seçmek için random.choice ve random.sample kullanımını optimize eder."""
    return random.sample(primes, 2)


def fermat_factorization(num, max_iterations=10**8):
    """Fermat'ın faktorizasyon algoritmasını uygular.

    Args:
        num (int): Faktörleri bulunacak sayı.
        max_iterations (int): Maksimum iterasyon sayısı.

    Returns:
        tuple: Bulunan çarpanlar veya None.
    """
    def is_square(n):
        """Bir sayının tam kare olup olmadığını kontrol eder."""
        sqrt_n = int(math.isqrt(n))  # math.isqrt ile tam sayı karekök
        return sqrt_n * sqrt_n == n

    a = int(math.isqrt(num)) + 1
    delta = a * a - num
    
    for i in range(max_iterations):
        if is_square(delta):
            b = int(math.isqrt(delta))
            return a - b, a + b, i  # Çarpanları ve iterasyon sayısını döndür
        a += 1
        delta = a * a - num

    return None, max_iterations


def fermat_factorization_limited(num, time_limit=25):
    """Fermat faktorizasyonu için zaman sınırı uygular.

    Args:
        num (int): Faktörleri bulunacak sayı.
        time_limit (int): Maksimum CPU zamanı (saniye).

    Returns:
        tuple: Bulunan çarpanlar veya None.
    """
    def is_square(n):
        sqrt_n = int(math.isqrt(n))
        return sqrt_n * sqrt_n == n

    a = int(math.isqrt(num)) + 1
    delta = a * a - num
    count = 0
    start_time = time.process_time()

    while not is_square(delta):
        if time.process_time() - start_time > time_limit:
            return None, count  # Zaman sınırı dolduysa None döndür
        a += 1
        delta = a * a - num
        count += 1

    b = int(math.isqrt(delta))
    return a - b, a + b, count


def check_result(n, factors):
    """Çarpanların doğruluğunu kontrol eder."""
    if factors is None or None in factors:
        return False
    p, q = factors[:2]
    return p * q == n


def run_fermat_factorizations(primes, num_tests=25):
    """Fermat faktorizasyonu ve zaman sınırlı faktorizasyonu bir dizi test üzerinde çalıştırır."""

    fermat_success = fermat_failure = 0
    llm_success = llm_failure = 0

    for _ in range(num_tests):
        p, q = random_prime_pair_choice(primes)
        n = p * q

        result_fermats = fermat_factorization(n)
        result_llm = fermat_factorization_limited(n)

        # Sonuçları doğrula
        if check_result(n, result_fermats):
            fermat_success += 1
        else:
            fermat_failure += 1
            print(f"Fermat faktorizasyonu başarısız: {result_fermats}, doğru çarpanlar: {p}, {q}")
        
        if check_result(n, result_llm):
            llm_success += 1
        else:
            llm_failure += 1
            print(f"Zaman sınırlı Fermat faktorizasyonu başarısız: {result_llm}, doğru çarpanlar: {p}, {q}")

    # Başarı ve başarısızlık oranlarını yazdır
    total_fermat = fermat_success + fermat_failure
    total_llm = llm_success + llm_failure

    fermat_failure_rate = (fermat_failure / total_fermat) * 100 if total_fermat > 0 else 0
    llm_failure_rate = (llm_failure / total_llm) * 100 if total_llm > 0 else 0

    print(f"Fermat faktorizasyonu başarısızlık oranı: {fermat_failure_rate:.2f}%")
    print(f"Zaman sınırlı Fermat faktorizasyonu başarısızlık oranı: {llm_failure_rate:.2f}%")


def main():
    primes = optimized_sieve_of_eratosthenes(10**8)
    run_fermat_factorizations(primes)


if __name__ == '__main__':
    main()
