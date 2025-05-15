import math
from bitarray import bitarray
import random
import time

def optimized_sieve_of_eratosthenes(limit):
    """Eratosthenes'in Eleği algoritmasının optimize edilmiş hali ile 2'den limit'e kadar olan asal sayıları bulur.

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
    for num in range(3, int(limit ** 0.5) + 1, 2):
        if is_prime[num]:
            # num'in katlarını işaretlerken çift sayıları atlıyoruz
            for multiple in range(num * num, limit + 1, num * 2):
                is_prime[multiple] = False

    # Asal sayılar listesi döndürülür
    return [2] + [num for num in range(3, limit + 1, 2) if is_prime[num]]


def choice_choice(liste):
    return random.choices(liste, k=2)


def choice_sample(liste):
    return random.sample(liste, 2)


def fermats_factorization(num):
    def is_square(n):
        """Bir sayının tam kare olup olmadığını kontrol eder."""
        sqrt_n = int(math.sqrt(n))
        return sqrt_n * sqrt_n == n

    a = int(math.sqrt(num)) + 1
    delta = a * a - num
    
    for i in range(10**8):
        #if math.sqrt(delta) - int(math.sqrt(delta)) == 0.:
        if is_square(delta):
            return a - int(math.sqrt(delta)), a + int(math.sqrt(delta)), str(i) + "-" + str(a)
        a += 1
        delta = a * a - num

    return None, 10**8


def fermats_factorization_llm(num):
    def is_square(n):
        """Bir sayının tam kare olup olmadığını kontrol eder."""
        sqrt_n = int(math.sqrt(n))
        return sqrt_n * sqrt_n == n


    a = int(math.ceil(math.sqrt(num)))  # a, num'un karekökünden büyük en küçük tam sayı
    b2 = a * a - num  # delta'yı b^2 olarak adlandıralım (b'nin karesi)
    count = 1

    start_cpu_time = time.process_time()  # CPU zamanı başlangıç noktası
    check_interval = 1000  # Zaman kontrolünü her 1000 iterasyonda bir yapacağız

    while not is_square(b2):
        if count % check_interval == 0:  # Belirli aralıklarla zaman kontrolü yap
            current_cpu_time = time.process_time()
            if current_cpu_time - start_cpu_time > 10:  # Eğer CPU süresi 10 saniyeyi aşarsa
                return None, count  # Süre sınırını aşıyorsa döngüden çık

        a += 1
        b2 = a * a - num
        count += 1

    b = int(math.sqrt(b2))  # b'yi bulalım
    return (a - b, a + b, count)


def check_result(n, factors):
    """Çarpanların doğru olup olmadığını kontrol eder."""
    if factors is None or None in factors:
        return False
    p, q = factors[:2]
    return p * q == n


def run_fermat_factorizations(primes):
    #86497711, 6448009
    #

    fermat_success = 0
    fermat_failure = 0
    llm_success = 0
    llm_failure = 0

    for _ in range(20):
        p1, q1 = choice_choice(primes)
        p2, q2 = choice_sample(primes)

        n1 = p1 * q1
        n2 = p2 * q2

        result1_fermats = fermats_factorization(n1)
        result1_llm = fermats_factorization_llm(n1)
        result2_fermats = fermats_factorization(n2)
        result2_llm = fermats_factorization_llm(n2)

        # Sonuçların doğruluğunu kontrol et
        if check_result(n1, result1_fermats):
            fermat_success += 1
        else:
            fermat_failure += 1
            print(f"n1 icin Fermat's factorization yanlis: {result1_fermats}, dogru çarpanlar: {p1}, {q1}")
        
        if check_result(n1, result1_llm):
            llm_success += 1
        else:
            llm_failure += 1
            print(f"n1 icin Fermat's factorization llm yanlis: {result1_llm}, dogru carpanlar: {p1}, {q1}")
        
        if check_result(n2, result2_fermats):
            fermat_success += 1
        else:
            fermat_failure += 1
            print(f"n2 icin Fermat's factorization yanlis: {result2_fermats}, dogru carpanlar: {p2}, {q2}")
        
        if check_result(n2, result2_llm):
            llm_success += 1
        else:
            llm_failure += 1
            print(f"n2 icin Fermat's factorization llm yanlis: {result2_llm}, dogru carpanlar: {p2}, {q2}")

    # Başarısızlık oranını hesapla
    fermat_total = fermat_success + fermat_failure
    llm_total = llm_success + llm_failure

    fermat_failure_rate = (fermat_failure / fermat_total) * 100 if fermat_total > 0 else 0
    llm_failure_rate = (llm_failure / llm_total) * 100 if llm_total > 0 else 0

    print(f"Fermat's factorization basarisizlik orani: {fermat_failure_rate:.2f}%")
    print(f"Fermat's factorization llm basarisizlik orani: {llm_failure_rate:.2f}%")


def main():
    primes = optimized_sieve_of_eratosthenes(10**8)
    run_fermat_factorizations(primes)

if __name__ == '__main__':
    main()

    """
    print(fermats_factorization(77))
    print()
    print(fermats_factorization(n1))
    print(p1, q1)
    print()
    print(fermats_factorization(n2))
    print(p2, q2)
    print()
    print(fermats_factorization_llm(77))
    print()
    print(fermats_factorization_llm(n1))
    print(p1, q1)
    print()
    print(fermats_factorization_llm(n2))
    print(p2, q2)
    """