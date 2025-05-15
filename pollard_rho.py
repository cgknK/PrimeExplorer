import math
import random
import sys

def pollard_rho(n, max_attempts=1000):
    if n % 2 == 0:
        return 2
    
    attempt = 0  # Maksimum döngü sayısını kontrol etmek için
    while attempt < max_attempts:
        # x, y, c rastgele seçiliyor
        x = random.randint(2, n - 1)
        y = x
        c = random.randint(1, n - 1)
        d = 1
        
        while d == 1:
            # x ve y için iterasyon yapılıyor
            x = (x**2 + c) % n
            y = (y**2 + c) % n
            y = (y**2 + c) % n
            d = math.gcd(abs(x - y), n)
        
        if d == n:  # Eğer d == n ise, sonsuz döngüde olabilir, yeniden başla
            attempt += 1
        elif d > 1:  # Eğer d > 1 ise, asal çarpan bulundu
            return d
    
    raise Exception(f"Pollard Rho failed after {max_attempts} attempts")

def factorize(n):
    factors = []
    
    while n > 1:
        factor = pollard_rho(n)
        factors.append(factor)
        n //= factor  # Bölme işlemi
    
    return factors

def count_factors(factors):
    factor_counts = {}
    for factor in factors:
        if factor in factor_counts:
            factor_counts[factor] += 1
        else:
            factor_counts[factor] = 1
    return factor_counts

# Test
n = 8 * 3
factors = factorize(n)
factor_counts = count_factors(factors)
print(f"Factors of {n}: {factor_counts}")
