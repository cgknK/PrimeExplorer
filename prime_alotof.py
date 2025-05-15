import math
import random
import time
import numpy as np
from bitarray import bitarray
import gc
from typing import List, Tuple, Optional


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
def classic_prime(n):
    if n < 2:
        return []
    primes = [2]
    for num in range(3, n+1, 2):
        if all(num % prime != 0 for prime in primes):
            primes.append(num)
    return primes


@cpu_time_decorator
def classic_prime_plus_sroot(n):
    if n < 2:
        return []
    primes = [2]
    for num in range(3, n + 1, 2):
        sqrt_num = int(num ** 0.5)
        if all(num % prime != 0 for prime in primes if prime <= sqrt_num): #gereksiz if prime <= sqrt_num
            primes.append(num)
    return primes


@cpu_time_decorator
def classic_prime_llm(n):
    if n < 2:
        return []
    primes = [2]
    for num in range(3, n + 1, 2):
        sqrt_num = int(num ** 0.5)
        is_prime = True
        for prime in primes:
            if prime > sqrt_num:
                #eğer break kullanmayarak classic_prime_plus_sroot eşitlersek classic_prime_llm yavaş kalıyor. Araştır.
                break  # Karekökten büyük asal sayılarla bölmeye gerek yok
            if num % prime == 0:
                is_prime = False
                break  # İlk bölen bulunduğunda durdur
        if is_prime:
            primes.append(num)
    return primes


@cpu_time_decorator
def classic_prime_llm_plus(n):
    if n < 2:
        return []
    primes = [2]
    for num in range(3, n + 1, 2):
        sqrt_num = int(num ** 0.5)
        is_prime = True

        if (num + 1) % 6 == 0 or (num - 1) % 6 == 0:
            if pow(2, num - 1, num) != 1:
                continue

        for prime in primes:
            if prime > sqrt_num:
                #eğer break kullanmayarak classic_prime_plus_sroot eşitlersek classic_prime_llm yavaş kalıyor. Araştır.
                break  # Karekökten büyük asal sayılarla bölmeye gerek yok
            if num % prime == 0:
                is_prime = False
                break  # İlk bölen bulunduğunda durdur
        if is_prime:
            primes.append(num)
    return primes


@cpu_time_decorator
def classic_prime_llm_plus_2(n):
    if n < 2:
        return []
    primes = [2]
    for num in range(3, n + 1, 2):
        sqrt_num = int(num ** 0.5)
        is_prime = True

        if pow(2, num - 1, num) != 1:
            continue

        for prime in primes:
            if prime > sqrt_num:
                #eğer break kullanmayarak classic_prime_plus_sroot eşitlersek classic_prime_llm yavaş kalıyor. Araştır.
                break  # Karekökten büyük asal sayılarla bölmeye gerek yok
            if num % prime == 0:
                is_prime = False
                break  # İlk bölen bulunduğunda durdur
        if is_prime:
            primes.append(num)
    return primes


@cpu_time_decorator
def pierre_de_fermat_s_little_theorem(n, k=25):
    """Fermat testi kullanarak n'e kadar olan asal sayıları bulur."""

    def fermat_is_prime(n, k):
        """Fermat'nın küçük teoremi ile asal sayı testi.
        
        Args:
            n (int): Test edilmek istenen sayı.
            k (int): Test sayısı. Daha büyük k, daha fazla doğruluk sağlar.
            
        Returns:
            bool: Sayı büyük olasılıkla asal ise True, değilse False.
        """
        if n < 4:
            return n == 3 or n == 2

        if pow(2, num - 1, num) != 1:
            return False

        # Fermat testi için k kez rastgele taban seçip test yapıyoruz
        #a_rand_list = np.random.randint(2, n-2, size=k)
        for _ in range(k): #561, 511 için min k bul.
            a = random.randint(2, n - 2)

            if math.gcd(a, n) != 1:
                return False  # Eğer gcd 1 değilse asal olamaz
            
            if pow(a, num - 1, num) != 1:
                return False
        return True

    if n < 2:
        return []
    
    primes = [2]
    
    # Yalnızca tek sayılar üzerinde ilerliyoruz
    for num in range(3, n + 1, 2):
        if fermat_is_prime(num, k):
            primes.append(num)
    
    return primes


@cpu_time_decorator
def pierre_de_fermat_s_little_theorem_lessfunccall(n, k=25):
    """Fermat testi kullanarak n'e kadar olan asal sayıları bulur."""
    
    if n < 2:
        return []
    
    primes = [2]
    
    # Yalnızca tek sayılar üzerinde ilerliyoruz
    for num in range(3, n + 1, 2):
        # num == 3 için özel bir kontrol yapmaya gerek yok, normal testten geçebilir
        if pow(2, num - 1, num) != 1:
            continue  # Fermat testi başarısız, asal değil
        
        is_prime = True
        # Fermat testi için k kez rastgele taban seçip test yapıyoruz
        for _ in range(k):  # k=5 olacak şekilde sabitledim
            if num - 2 < 3:
                break

            a = random.randint(3, num - 2)

            if math.gcd(a, num) != 1:
                is_prime = False
                break 

            if pow(a, num - 1, num) != 1:
                is_prime = False
                break
        
        if is_prime:
            primes.append(num)
    
    return primes


@cpu_time_decorator
def hibrit_fermat_classic(num):
    
    def is_prime(n):
        sqrt_num = int(n ** 0.5)
        for i in range(3, sqrt_num + 1, 2):
            if n % i == 0:
                return False
        return True

    primes = []
    slack_result = pierre_de_fermat_s_little_theorem(num, k=0)

    for n in slack_result:
        if is_prime(n):
            primes.append(n)

    return primes


@cpu_time_decorator
def hybrid_fermat_classic_2(n, k=1):
    """Hibrit Fermat ve klasik asal testi ile asal sayıları bulur."""
    
    def is_prime_classic(num):
        """Klasik asal sayı testi (bölme metodu)."""
        sqrt_num = int(num ** 0.5)
        for i in range(3, sqrt_num + 1, 2):
            if num % i == 0:
                return False
        return True

    def fermat_is_prime(num, k):
        """Fermat testi ile asal sayı kontrolü."""
        if num < 4:
            return num == 3 or num == 2
        
        # Fermat testi (modüler üs)
        if pow(2, num - 1, num) != 1:
            return False
        
        # Fermat testi için rastgele k baz seçip kontrol ediyoruz
        for _ in range(k):
            a = random.randint(2, num - 2)
            if math.gcd(a, num) != 1:
                return False
            if pow(a, num - 1, num) != 1:
                return False
            if not is_prime_classic(num):
                return False
        return True

    if n < 2:
        return []

    primes = [2]
    
    for num in range(3, n + 1, 2):
        if fermat_is_prime(num, k):
                primes.append(num)
    
    return primes

@cpu_time_decorator
def miller_rabin(num):
    class MillerRabinTest:
        def __init__(self, num_rounds=5):
            """
            Miller-Rabin testini başlatır.
            :param num_rounds: Asal olup olmadığını kontrol etmek için kaç taban kullanılacağı (varsayılan 5)
            """
            if num_rounds < 1:
                raise ValueError("Number of rounds must be at least 1")
            self.num_rounds = num_rounds

        def is_prime(self, n):
            """
            Sayının asal olup olmadığını Miller-Rabin testi ile kontrol eder.
            :param n: Test edilecek sayı
            :return: True (muhtemelen asal), False (kesinlikle bileşik)
            """
            if n < 2:
                return False
            if n == 2 or n == 3:
                return True
            if n % 2 == 0:
                return False
            
            # n-1 = 2^s * d olacak şekilde yaz
            s, d = self._decompose(n - 1)
            
            # num_rounds kadar rastgele taban seç ve testi yap
            for _ in range(self.num_rounds):
                a = random.randint(2, n - 2)
                if not self._miller_rabin_test(n, a, d, s):
                    return False
            return True

        def _decompose(self, n_minus_1):
            """
            n-1 sayısını 2^s * d şeklinde yazmak için parçalar.
            :param n_minus_1: n - 1 sayısı
            :return: s ve d değerleri
            """
            s = 0
            d = n_minus_1
            while d % 2 == 0:
                d //= 2
                s += 1
            return s, d

        def _miller_rabin_test(self, n, a, d, s):
            """
            Miller-Rabin testi adımını gerçekleştirir.
            :param n: Test edilen sayı
            :param a: Rastgele seçilen taban
            :param d: n-1'in tek olan kısmı
            :param s: n-1'in 2'ye bölünme sayısı
            :return: True (muhtemelen asal), False (kesinlikle bileşik)
            """
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                return True
            for _ in range(s - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    return True
            return False

    test = MillerRabinTest()
    primes = []
    
    for i in range(2, num + 1):
        if test.is_prime(i):
            primes.append(i)
    
    return primes


@cpu_time_decorator
def eratosthenes_sieve(n):
    primes = [2]
    sieve = [True] * (n+1) # bu kısım ve döngü indeksi ayarlanarak n/2 uzay karmaşıklığı tasarufu sağlanabilir.
    for p in range(3, n+1, 2):
        if sieve[p]:
            primes.append(p)
            for i in range(p*p, n+1, p):
                sieve[i] = False
    return primes


@cpu_time_decorator
def eratosthenes_sieve_2(n):
    asal = [True] * (n + 1)
    asal[0], asal[1] = False, False

    for bolen in range(2, int(n**0.5) + 1):
        if asal[bolen]:
            for kat in range(bolen * bolen, n + 1, bolen):
                asal[kat] = False

    asal_sayisi = sum(asal)
    print(f"1'den {n}'e kadar {asal_sayisi} adet asal sayi var.")
    return asal_sayisi

def logaritmik_sarmal_yaniendusukdirenctasarimi_math(num):
    dens_prime = 1 / (math.log(num))
    return dens_prime * num

@cpu_time_decorator
def sieve_of_eratosthenes(limit):
    """Eratosthenes'in Eleği algoritması ile 2'den limit'e kadar olan asal sayıları bulur.

    Args:
        limit (int): Asal sayıların bulunacağı üst sınır.

    Returns:
        list: Bulunan asal sayıların listesi.
    """
    if limit < 2:
        return []

    # Başlangıçta 2 hariç tüm çift sayılar False olarak işaretlenir
    is_prime = [False, False, True] + [True, False] * (limit // 2)
    #is_prime = [True] * limit
    #is_prime[0], is_prime[1], is_prime[2] = False, False, True
    #print(len(is_prime))
    # is_prime = is_prime[:limit + 1] #veya if ile ayarlanabilir #Test için 210

    # 2 asal olduğu için elle işaretlenir
    is_prime[2] = True

    # Yalnızca tek sayılar için işlem yapılır
    for num in range(3, int(limit ** 0.5) + 1, 2):
        if is_prime[num]:
            for multiple in range(num * num, limit + 1, num * 2):
                is_prime[multiple] = False

    # Asal sayılar listesi döndürülür
    return [num for num, prime in enumerate(is_prime) if prime]
    #return [2] + [num for num in range(3, len(is_prime), 2) if is_prime[num]]


@cpu_time_decorator
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


@cpu_time_decorator
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


@cpu_time_decorator
def sieve_of_sundaram_hatali(length): #hatalı
    #https://plus.maths.org/content/sundarams-sieve, kanıt bulamadım.

    primes = [2]

    loop_sentinel = (length - 1) // 2
    non_primes = set()  # asal olmayan sayıları burada tutacağız
    
    for i in range(1, loop_sentinel + 1):
        for j in range(1, i + 1):
            result_formula = i + j + 2 * i * j
            if result_formula >= loop_sentinel:
                break
            non_primes.add(result_formula)

    for i in range(1, loop_sentinel + 1):
        if i not in non_primes:
            primes.append(2 * i + 1)

    return primes


@cpu_time_decorator
def sieve_of_sundaram(length):#MAntık?
    primes = [True] * (length // 2 + 1)
    primes[0] = False

    for i in range(1, length // 2 + 1):
        for j in range(1, i + 1):
            num = i + j + 2 * i * j
            if i + j + 2 * i * j > length // 2:
                break
            primes[num] = False

    return [2] + [2 * i + 1 for i in range(len(primes)) if primes[i]]
    #return [2 * i + 1 for i, e in enumerate(primes) if e]


@cpu_time_decorator
def sieve_of_sundaram_2(length):
    loop_sentinel = (length - 1) // 2
    sieve = [False] * (loop_sentinel + 1)

    for i in range(1, loop_sentinel + 1):
        for j in range(i, (loop_sentinel - i) // (2 * i + 1) + 1):
            result_formula = i + j + 2 * i * j
            if result_formula <= loop_sentinel:
                sieve[result_formula] = True

    primes = [2]
    for i in range(1, loop_sentinel + 1):
        if not sieve[i]:
            primes.append(2 * i + 1)

    return primes


@cpu_time_decorator
def sieve_of_atkin(n):#10^6 veya 7'den sonra neden sieve_of_eratosthenes'den daha yavaş?
    is_primes = [False] * (n + 1)
    sqrt = int(math.sqrt(n))

    for x in range(1, sqrt + 1):
        for y in range(1, sqrt + 1):
            temp = 4 * x * x + y * y
            if temp <= n and (temp % 12 == 1 or temp % 12 == 5):
                is_primes[temp] = not is_primes[temp]

            temp = 3 * x * x + y * y
            if temp <= n and (temp % 12 == 7):
                is_primes[temp] = not is_primes[temp]

            temp = 3 * x * x - y * y
            if x > y and temp <= n and (temp % 12 == 11):
                is_primes[temp] = not is_primes[temp]

    for i in range(5, sqrt + 1):
        if is_primes[i]:
            temp = i * i
            for j in range(temp, n + 1, temp):
                is_primes[j] = False

    primes = [2, 3] + [i for i in range(5, len(is_primes), 2) if is_primes[i]]
    return primes


@cpu_time_decorator
def elliptic_curve_primality_proving_ECPP(num):
    from sympy import isprime, mod_inverse, divisors
    from math import gcd

    class EllipticCurve:
        def __init__(self, a: int, b: int):
            self.a = a
            self.b = b
            self.discriminant = -16 * (4 * a**3 + 27 * b**2)

        def is_smooth(self) -> bool:
            """Eğer discriminant sıfır değilse eğri düzgündür."""
            return self.discriminant != 0

        def point_on_curve(self, x_val: int, y_val: int) -> bool:
            """Verilen bir noktanın eğri üzerinde olup olmadığını kontrol eder."""
            return y_val**2 == x_val**3 + self.a * x_val + self.b

    def gcd_test(factor: int, num: int) -> bool:
        """GCD'nin 1 olup olmadığını test eder."""
        return gcd(factor, num) == 1

    def mod_inverse_test(factor: int, num: int) -> bool:
        """Modüler tersin olup olmadığını test eder."""
        try:
            mod_inverse(factor, num)
            return True
        except ValueError:
            return False

    def elliptic_curve_primality_proving_ECPP(num: int) -> bool:
        """
        Verilen sayının ECPP algoritması ile asal olup olmadığını test eder.
        """
        if num <= 1:
            return False

        #if isprime(num):
            #return True  # Eğer sayı SymPy'de asal ise direkt True döner.

        # Rastgele elliptik eğri seçimi
        a, b = 2, 3  # y^2 = x^3 + 2x + 3 eğrisi
        curve = EllipticCurve(a, b)

        # Eğrinin düzgün olup olmadığı kontrol edilir
        if not curve.is_smooth():
            return False

        # Birkaç rastgele noktayı test etmek için döngü
        for x_val in range(1, 100):  # 100'e kadar rastgele x değeri alıyoruz
            for y_val in range(1, 100):  # y değerleri de rastgele seçilir
                if curve.point_on_curve(x_val, y_val):
                    # Eğer nokta eğri üzerinde ise, num'un küçük bölenlerini kontrol et
                    for factor in divisors(num):
                        if 1 < factor < num:
                            # GCD testi ve modüler ters testi
                            if not gcd_test(factor, num) or not mod_inverse_test(factor, num):
                                return False
        return True

    def find_primes_up_to(limit: int) -> list:
        """
        Verilen sınıra kadar ECPP ile asal sayıları bulur.
        """
        return [num for num in range(2, limit + 1) if elliptic_curve_primality_proving_ECPP(num)]

    primes = find_primes_up_to(num)
    return primes


@cpu_time_decorator
def baillie_PSW_llm(num):#çalışmıyor doesntWork
    """Baillie-PSW asallık testi.
    Miller-Rabin ve Lucas testleri uygulanarak sayı asal mı kontrol edilir.
    
    Args:
        num (int): Asallığı test edilecek sayı.
    
    Returns:
        bool: Sayı asal ise True, değilse False döner.
    """
    # def lucas_lehmer_test(n):
    def miller_rabin(n, k=5):
        """Miller-Rabin asallık testi.
        
        Args:
            n (int): Asallığı test edilecek sayı.
            k (int): Test tekrar sayısı. Default 5.
        
        Returns:
            bool: Sayı Miller-Rabin testini geçerse True, geçemezse False.
        """
        if n % 2 == 0:
            return False
        
        # n-1 = 2^r * s olacak şekilde yazılır
        r, s = 0, n - 1
        while s % 2 == 0:
            r += 1
            s //= 2
        
        # k kez rastgele tabanlar seçilerek test edilir
        for _ in range(k):
            a = random.randint(2, n - 1)
            x = pow(a, s, n)
            if x == 1 or x == n - 1:
                continue
            # x^2 mod n hesaplanır, n-1'e eşit olduğunda asal olabilir
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        
        return True

    def lucas_test(n):
        """Lucas asallık testi.
        
        Args:
            n (int): Asallığı test edilecek sayı.
        
        Returns:
            bool: Lucas testini geçerse True, geçemezse False.
        """
        if n == 2:
            return True
        if n % 2 == 0:
            return False

        # Uygun D değeri seçimi
        def calculate_d(n):
            D = 5
            while True:
                jacobi = pow(D, (n - 1) // 2, n)
                if jacobi == n - 1:
                    break
                D = -D - 2 if D > 0 else -D + 2
            return D

        D = calculate_d(n)
        
        # Lucas dizisi ile test yapılır
        P, Q = 1, (1 - D) // 4
        U, V = 1, P
        k = n + 1

        for bit in bin(k)[3:]:
            U, V = (U * V) % n, (V * V - 2 * Q) % n
            if bit == '1':
                U, V = (P * U + V) % n, (D * U + P * V) % n
        
        # Sonuç kontrol edilir
        return U == 0

    # Adım 1: Küçük sayılar için kontrol
    if num < 2:
        return False
    if num in [2, 3, 5, 7]:
        return True
    if any(num % p == 0 for p in [2, 3, 5, 7]):
        return False

    # Adım 2: Miller-Rabin testini uygula
    if not miller_rabin(num):
        return False

    # Adım 3: Lucas testini uygula
    if not lucas_test(num):
        return False

    # Eğer her iki testi de geçerse sayı asal kabul edilir
    return True


def solovay_strassen_test(n, k=2**20):
    def jacobi(a, num):
        if math.gcd(a, num) != 1:
            return 0#genelleştirilmiş Legendre sembolü

        if 0 == a:
            return 0

        a = a % num
        
        if 1 == a:
            return 1
        
        if a % 2 == 0: # a | 2^k*m = a
            return (-1)**((num**2 - 1) // 8) * jacobi(a // 2, num)

        #Reciprocity Law
        # kuadratik karşılıklılık yasası
        if a % 2 == 1 and num % 2 == 1:
            return (-1)**((a-1) * (num-1) / 4) * jacobi(num, a)


    if n < 2:
        return False

    if n == 2:
        return True
    # 1/2^k hata oranı, k iterasyon adedi, default yaklaşık milyonda 1 hata
    while k > 1:
        a = random.randint(2, n - 1)
        #if jacobi(a, n) % n != (a**((n-1) / 2) % n):
        if jacobi(a, n) % n != pow(a, (n - 1) // 2, n):
            return False
        k -= 1

    return True


def aks_prime_test_meUndLlm(n):
    #(x−a)^p denk x^p-a mod p
    #Agrawal, Kayal, Saxena

    def multiplicative_order(r_min, r_limit, n):
        """r_min'ten başlayarak, n'e göre r modülünde döngüsel birimleri arıyoruz."""

        def euler_totient(r):
            count = 0
            for i in range(1, r):
                if gcd(i, r) == 1:
                    count += 1
            return count

        def is_prime(num):
            """Asal sayı kontrolü."""
            if num <= 1:
                return False
            for i in range(2, int(math.sqrt(num)) + 1):
                if num % i == 0:
                    return False
            return True

        log2_n = math.log(n, 2)
        
        for r in range(r_min, int(r_limit) + 1):
            if not is_prime(r):  # r'nin asal olup olmadığını kontrol et
                continue
            
            if math.gcd(n, r) != 1:  # n ve r aralarında asal olmalı
                return -1  # gcd(n, r) > 1 olduğunda sayının asal olmadığını döneriz

            order = 1
            while pow(n, order, r) != 1 and order <= log2_n:
                order += 1

            # Eğer o(n) > log2(n) ise doğru r'yi bulduk demektir
            if order > log2_n:
                return r
            
        return -1  # Eğer uygun bir r bulunamazsa


    if n < 2:
        return False

    n_sqrt = math.isqrt(n)
    if n_sqrt * n_sqrt == n:
        return False

    mini_primes = [2]#[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for prime in mini_primes:
        if n % prime == 0:
            return n == prime

    _r_limit = math.log(n) ** 2
    _r_min = int(math.log(n))

    r_min = multiplicative_order(_r_min, _r_limit, n)
    if r_min == -1:
        return False

    # Eğer gcd(a, n) > 1 ve 1 < a ≤ r_min ise asal değildir.
    for a in range(2, r_min + 1):
        if math.gcd(a, n) > 1:
            return False
    
    # Polinom kontrolü: (x - a)^n ≡ (x^n - a) mod (x^r - 1, n) doğruluğunu kontrol et.
    # Bu adım Fermat'ın Küçük Teoreminin genişletilmiş haline dayanır.
    for a in range(1, min(r_min, n)):
        lhs = (pow(a, n, n) - a) % n
        if lhs != 0:
            return False

    # Son adım: Eğer n, r_min'den küçükse, asal olduğunu varsayıyoruz.
    if n <= r_min:
        return True
    
    return True


def aks_prime_test_bilkav(n):
    """
    https://bilgisayarkavramlari.com/2011/04/13/aks-asallik-testi-aks-primality-test/
    https://bilgisayarkavramlari.com/2011/04/13/carpim-derecesi-multiplicative-order/
    """

    def is_prime(num):
        if num <= 1:
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True

    def multiplicative_order(r, n):
        if math.gcd(n, r) != 1:  # Aralarında asal değilse -1 döndür
            return -1

        durum = n
        derece = 1
        while durum % r != 1:
            durum *= n
            derece += 1
            if derece > r:
                return -1

        return derece

    if n == 2:
        return True
    if n < 2:
        return False

    n_sqrt = math.isqrt(n)
    if n_sqrt * n_sqrt == n:
        return False

    logn = math.log(n, 2)
    r = 2
    while r < n:
        if math.gcd(n, r) != 1:
            return False

        if aks_prime_test_bilkav(r):
            q = multiplicative_order(n, r)

            if q >= 4 * logn * math.sqrt(r) and pow(n % r, (r - 1) / q) != 1:
                break

        r += 1
        while not is_prime(r):
            r += 1


    for a in range(1, int(2 * math.sqrt(r) * logn) + 1):
        if (a - a % n) % pow(pow(a, r - 1), n) != (pow(a, n) - a % n) % pow(a, r - 1):
            return False

    return True


    
# Multiplicative Order Function
def multiplicative_order(n, r):
    if gcd(n, r) != 1:  # Eğer n ile r aralarında asal değilse -1 döndür
        return -1

    phi_r = euler_totient(r)  # Euler Totient fonksiyonu ile φ(r) hesapla
    durum = 1  # Başlangıç değeri
    derece = 0  # Üs sayacı

    while derece <= phi_r:  # Dereceyi φ(r) sınırına kadar deneyebiliriz
        derece += 1
        durum = (durum * n) % r  # Her seferinde mod r alınarak ilerlenir
        if durum == 1:  # Eğer sonuç 1 olursa çarpımsal dereceyi bulduk demektir
            return derece

    return -1  # Eğer φ(r) sınırına kadar çözüm bulamazsak, çarpımsal derece yoktur
    

def pocklington_primality_test(num, k=2):
    if num < 2:
        return num, False

    if num == 2 or num == 3:
        return num, True

    a = 2
    q = 0
    while k > 0:
        for i in range(2, num - 1):
            q = math.gcd(i, num - 1)
            if q > 1:
                break

        if q == 0:
            print("q==0", num)
            return num, False

        if a ** (num - 1) % num != 1:
            return num, False
        if a ** (num - 1) // q % num == 1:
            return num, False
        a = random.randint(2, num - 1)
        k -= 1

    return num, True


@cpu_time_decorator
def wheel_sieve(limit: int) -> List[int]:
    if limit < 2:
        return []

    base_primes = [2, 3, 5]
    if limit in base_primes:
        return base_primes[:limit]

    base_mod = math.prod(base_primes) #reduce(lambda x, y: x * y, base_primes)
    whell_pattern = [7, 11, 13, 17, 19, 23, 29, 31]

    total_candidate = []#[i * 30 + j for i in range(limit // base_mod + 1) for j in whell_pattern if i * 30 + j <= limit]

    for i in range(limit // base_mod + 1):
        for j in whell_pattern:
            temp = i * 30 + j
            if temp > limit:
                #print(i, j, i * 30 + j, i * 30)
                break
            total_candidate.append(temp)


    #return base_primes + total_candidate
    #print(total_candidate)

    #is_prime = np.zeros(limit + 1, dtype=bool)
    #is_prime[2] = True
    #is_prime[3:limit + 1:2] = True  # Tüm tek sayılar asal varsayılır

    #total_candidate = base_primes + total_candidate
    #print("->", total_candidate)
    #dump = []
    #print(total_candidate)
    #for num in range(3, int(math.sqrt(limit)) + 1, 30):
    for e in total_candidate:
        k = e * e
        #dump.append((k, e))
        if k > limit:
            break
        if k % 2 == 0 or k % 3 == 0 or k % 5 == 0:
                continue
        if k in total_candidate:
                total_candidate.remove(k)
        while k <= total_candidate[-1]:
            k += e # += 30 # *= 30
            if k % 2 == 0 or k % 3 == 0 or k % 5 == 0:
                continue
            if k in total_candidate:
                total_candidate.remove(k)
            #dump.append((k, e))
    #print("->", dump)

    #return np.nonzero(is_prime)[0].tolist()  # Asal sayıların listesini döndür
    return base_primes + total_candidate


"""
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
"""
@cpu_time_decorator
def wheel_sieve_optimized(limit: int) -> List[int]:
    if limit < 2:
        return []

    base_primes = np.array([2, 3, 5])
    if limit in base_primes:
        limit_index = np.where(base_primes == limit)[0][0]
        return base_primes[:limit_index + 1]

    base_mod = np.prod(base_primes) #reduce(lambda x, y: x * y, base_primes)
    whell_pattern = np.array([7, 11, 13, 17, 19, 23, 29, 31])

    # i * 30 işlemi için aralık oluştur
    i_values = np.arange(0, limit // base_mod + 1) * 30
    # Her i değeri için whell_pattern'i toplama işlemi yaparak sonuçları hesapla
    total_candidates = i_values[:, None] + whell_pattern

    # limit değerine göre filtrele (limitten büyük olanları at)
    total_candidates = total_candidates[total_candidates <= limit]#.flatten()

    # Asal olup olmadığını takip eden boolean maske
    is_prime = np.ones_like(total_candidates, dtype=bool)

    for e in total_candidates:
        k = e * e
        if k > limit:
            break

        if k % 2 == 0 or k % 3 == 0 or k % 5 == 0:
            continue
        # Asal olmayanları False olarak işaretle
        is_prime[(total_candidates >= k) & (total_candidates % e == 0)] = False
        """
        while k <= total_candidates[-1]:
            if k in total_candidates:
                total_candidates = total_candidates[total_candidates != k]
            k += e # += 30 # *= 30
        """

    #return np.nonzero(is_prime)[0].tolist()  # Asal sayıların listesini döndür
    return  np.concatenate((base_primes, total_candidates[is_prime])).tolist()


@cpu_time_decorator
def wheel_sieve_optimized_2(limit: int) -> List[int]:
    if limit < 2:
        return []

    # Base prime numbers for 30-wheel (2, 3, 5 are handled separately)
    base_primes = np.array([2, 3, 5], dtype=np.uint32)

    # If limit is small enough, return the base primes directly
    if limit <= 5:
        return base_primes[base_primes <= limit].tolist()

    # Initialize the wheel: numbers that are coprime with 2, 3, and 5
    wheel_pattern = np.array([7, 11, 13, 17, 19, 23, 29, 31], dtype=np.uint32)

    # Boolean array to mark prime numbers up to limit
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[:2] = False  # 0 and 1 are not prime

    # Mark multiples of 2, 3, and 5 as non-prime
    for p in base_primes:
        is_prime[p * p:limit+1:p] = False

    # Process the rest using the wheel
    for num in range(7, int(limit**0.5) + 1, 2):
        if is_prime[num]:
            is_prime[num * num:limit + 1:num * 2] = False

    # Collect all prime numbers
    primes = np.nonzero(is_prime)[0].tolist()

    return primes


# Python3 program to check if the
# given number is prime using
# Wheel Factorization Method
import math

# Function to check if a given
# number x is prime or not
def isPrime_Wheel_Factorization_Algorithm(N):
    #https://www.geeksforgeeks.org/wheel-factorization-algorithm/

    isPrime = True;
    # The Wheel for checking
    # prime number
    arr= [ 7, 11, 13, 17,
                19, 23, 29, 31 ]

    # Base Case
    if (N < 2) :
        isPrime = False

    # Check for the number taken
    # as basis
    if (N % 2 == 0 or N % 3 == 0
        or N % 5 == 0):
        isPrime = False

    # Check for Wheel
    # Here i, acts as the layer
    # of the wheel
    for i in range(0,int(math.sqrt(N)), 30) :

        # Check for the list of
        # Sieve in arr[]
        for c in arr:

            # If number is greater
            # than sqrt(N) break
            if (c > int(math.sqrt(N))):
                break

            # Check if N is a multiple
            # of prime number in the
            # wheel
            else :
                if (N % (c + i) == 0) :
                    isPrime = False
                    break

            # If at any iteration
            # isPrime is false,
            # break from the loop
            if (not isPrime):
                break

    if (isPrime):
        print("Prime Number")
    else:
        print("Not a Prime Number")


def main():
    length = 10**9 #2**29#2**32# 561, 127, 31
    length = int(length)
    #result_classic_prime = classic_prime(length)
    #result_classic_prime_plus_sroot = classic_prime_plus_sroot(length)
    #result_classic_prime_llm = classic_prime_llm(length)
    #result_classic_prime_llm_plus = classic_prime_llm_plus(length)
    #result_classic_prime_llm_plus_2 = classic_prime_llm_plus_2(length)
    #result_pierre_de_fermat_fermat_s_little_theorem = pierre_de_fermat_s_little_theorem(length)
    #result_pierre_de_fermat_s_little_theorem_lessfunccall = pierre_de_fermat_s_little_theorem_lessfunccall(length)
    #result_hibrit_fermat_classic = hibrit_fermat_classic(length)
    #result_hybrid_fermat_classic_2 = hybrid_fermat_classic_2(length)
    #result_miller_rabin = miller_rabin(length)
    #result_eratosthenes_sieve = eratosthenes_sieve(length)
    #result_eratosthenes_sieve_2 = eratosthenes_sieve_2(length)
    #result_sieve_of_eratosthenes = sieve_of_eratosthenes(length)
    #del result_sieve_of_eratosthenes
    #gc.collect()
    #result_optimized_sieve_of_eratosthenes = optimized_sieve_of_eratosthenes(length)
    result_optimized_sieve_of_eratosthenes_numpy = optimized_sieve_of_eratosthenes_numpy(length)
    #del result_optimized_sieve_of_eratosthenes
    #gc.collect()
    #result_sieve_of_sundaram_hatali = sieve_of_sundaram_hatali(length)
    #result_sieve_of_sundaram = sieve_of_sundaram(length)
    #result_sieve_of_sundaram_2 = sieve_of_sundaram_2(length)
    #result_sieve_of_atkin = sieve_of_atkin(length)
    #result_elliptic_curve_primality_proving_ECPP = elliptic_curve_primality_proving_ECPP(length)
    #result_baillie_PSW_llm = baillie_PSW_llm(17)
    #print(result_baillie_PSW_llm)
    #result_wheel_sieve = wheel_sieve(length)
    #result_wheel_sieve_optimized = wheel_sieve_optimized(length)
    result_wheel_sieve_optimized_2 = wheel_sieve_optimized_2(length)

    for prime in result_optimized_sieve_of_eratosthenes_numpy[95:109]:
        temp = solovay_strassen_test(prime, k=1)
        if temp:
            print(prime, temp, end=" - ")
            break
        else:
            print("\t", prime, temp)
    print("\n" * 2)

    #print("meUndLlm", aks_prime_test_meUndLlm(503))
    #print("bilkav", aks_prime_test_bilkav(503))

    pocklington_primality_false_positive_test = [2, 3, 7, 31, 341, 503, 561, 645, 1105]
    for e in pocklington_primality_false_positive_test:
        print(pocklington_primality_test(e, 10))



    print("\n" * 2)
    #print(result_optimized_sieve_of_eratosthenes_numpy == result_wheel_sieve)
    #print(len(result_optimized_sieve_of_eratosthenes_numpy) - len(result_wheel_sieve))
    #print(result_optimized_sieve_of_eratosthenes_numpy == result_wheel_sieve_optimized)
    print(result_optimized_sieve_of_eratosthenes_numpy == result_wheel_sieve_optimized_2)
    #print(result_wheel_sieve_optimized)
    #print(result_wheel_sieve_optimized_2)

    #dens_prime for test


if __name__ == '__main__':
    main()









if False:
    n = 10_000_000
    asal_mi = [True] * (n + 1)
    asal_mi[0], asal_mi[1] = False, False

    # n'in kareköküne kadar olan sayılar için asal kontrolü yapılıyor.
    for bolen in range(2, int(n**0.5) + 1):
        if not asal_mi[bolen]:
            continue
        for kat in range(bolen * bolen, n + 1, bolen):
            asal_mi[kat] = False

    # Asal sayıların sayısını hesaplıyoruz.
    asal_sayisi = sum(asal_mi)

    print(f"1'den {n}'e kadar {asal_sayisi} adet asal sayı var.")


    """
    cython --embed -o my_code.c my_code.py
    gcc -S my_code.c
    """


def list_diff(list1, list2):
    b = [1, 2, 3, 4, 5, 3, ]
    a = [2, 3]
    c = [elem for elem in b if elem not in a]
    print(c)
    from collections import Counter
    counter_b = Counter(b)
    counter_a = Counter(a)
    result = list((counter_b - counter_a).elements())
    print(result)

    print(result_pierre_de_fermat_fermat_s_little_theorem[-10:])
    print("dogruMu", result_pierre_de_fermat_fermat_s_little_theorem == result_classic_prime_plus_sroot)
    print(len(result_classic_prime_plus_sroot), len(result_pierre_de_fermat_fermat_s_little_theorem))
    print([i for i in range(len(result_pierre_de_fermat_fermat_s_little_theorem)) 
           if result_classic_prime_plus_sroot[i] != result_pierre_de_fermat_fermat_s_little_theorem[i]])

def Euler_totient():
    def phi():
        pass



"""
1. Güçlü Asallar (Strong Primes)

    Tanım: Güçlü asal sayılar, belirli matematiksel özelliklere sahip asal sayılardır. Güçlü asal, rastgele bir asal sayıdan daha güvenli kabul edilir çünkü bu sayılar, RSA'nın saldırılara karşı daha dayanıklı olmasını sağlar.
    Matematiksel Özellikler:
        Güçlü asal sayılar, genellikle p−1p−1 ve p+1p+1 sayılarının büyük asal çarpanları olması ile karakterize edilir.
        Örneğin, pp bir güçlü asal ise, hem p−1p−1 hem de p+1p+1'in büyük asal çarpanlara sahip olması beklenir.
    Saldırılara Karşı Dayanıklılık: RSA'da kullanılan asal sayılar, asal çarpanlarına ayrılmaya çalışıldığında (faktörizasyon saldırıları), güçlü asallar bu işlemi daha zor hale getirir. Özellikle Pollard p-1 gibi algoritmalar, p−1p−1'in asal çarpanlarının küçük olması durumunda faktörizasyonu hızlandırabilir. Güçlü asallar, bu tarz saldırılara karşı daha dirençlidir.

2. Faktörizasyonu Zorlaştıran Özellikler

RSA algoritmasının güvenliği, iki büyük asal sayının çarpımının faktörizasyonunun zor olmasına dayanır. Bazı özel asal sayılar bu süreci daha da zorlaştırabilir:

    Blum Asalları (Blum Primes): Blum asal sayıları, p≡3 (mod 4)p≡3 (mod 4) şeklinde ifade edilen asal sayılardır. Bu tür asal sayılar, bazı kriptografik algoritmalarda faktörizasyonu zorlaştırıcı bir özellik sunar.
    Çift Asallar (Safe Primes): Bir asal sayı pp, hem kendisi hem de (p−1)/2(p−1)/2 asal ise buna çift asal (safe prime) denir. Çift asallar, faktörizasyon algoritmalarını zorlaştırmada önemli bir rol oynar.

3. Lenstra ve Pollard Saldırılarına Karşı Koruma

RSA algoritmasına yönelik belirli saldırılar vardır. Asal sayılar bu saldırılara karşı korunmalıdır:

    Pollard p-1 Algoritması: Bu saldırı, asal sayı pp'nin p−1p−1'inin küçük asal çarpanlara sahip olması durumunda başarılı olabilir. Yukarıda bahsedilen güçlü asallar bu tür saldırılara karşı koruma sağlar.
    Lenstra ECM (Elliptic Curve Method) Saldırısı: Eliptik eğri faktörizasyon metodu (ECM), özellikle zayıf asal çarpanlara sahip büyük bileşik sayılar için etkilidir. RSA'da kullanılacak asal sayılar, bu saldırıya karşı dirençli olmalıdır. Bu yüzden, seçilen asal sayılar büyük ve rastgele olmalı, belirli bir yapıya sahip olmamalıdır.

4. Carmichael Sayıları ve Diğer Yalancı Asal Saldırıları

Carmichael sayıları, asal sayılara çok benzer özellikler gösteren bileşik sayılardır. Eğer bir RSA sistemi Carmichael sayıları kullanırsa, sistemin güvenliği tehlikeye girebilir. RSA'da kullanılan asal sayılar, bu tür bileşik sayılardan korunmak için dikkatlice seçilmelidir. Bu nedenle asal sayıları test ederken daha güçlü asal sayılık testleri kullanılır.
5. Yan-Kanal Saldırılarına Karşı Koruma (Side-Channel Attacks)

Asal sayılar doğrudan bu saldırılara karşı koruma sağlamasa da, RSA algoritmasında kullanılan asal sayıların seçimi ve algoritmanın uygulanışı, yan-kanal saldırılarını zorlaştırıcı ek önlemler içermelidir. Örneğin, asal sayıların seçimi rastgeleleştirilirken zamana dayalı veya güç tüketimine dayalı izlemeleri zorlaştırmak için çeşitli önlemler alınabilir.
6. Eşit Boyutta Asallar (Balanced Primes)

Güvenlik açısından RSA'da kullanılan asal sayılar genellikle aynı büyüklükte seçilir. İki asal sayının boyutu arasındaki farkın fazla olması, faktörizasyon saldırılarını kolaylaştırabilir. Örneğin, pp ve qq'nun boyutları arasında büyük farklar varsa, bu saldırıları hızlandırabilir.
7. Çok Büyük Bit Uzunluğu

Asal sayılar ne kadar büyükse, RSA'nın güvenliği o kadar yüksek olur. Ancak daha büyük asal sayılar performansı düşürebilir. Modern RSA implementasyonlarında genellikle 2048 bit ve üstü asal sayılar kullanılır. RSA-4096 gibi daha büyük bit uzunlukları ise daha yüksek güvenlik gerektiren uygulamalar için tercih edilir.
"""
