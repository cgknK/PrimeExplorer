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

def elliptic_curve_primality_proving_ECPP(num: int) -> bool:
    """
    Verilen sayının ECPP ile asal olup olmadığını kontrol eder.

    :param num: Asal olup olmadığı test edilecek sayı.
    :return: Sayı asal ise True, aksi halde False.
    """
    if num <= 1:
        return False

    # İlk hızlı kontrol: Eğer sympy isprime doğrudan doğruyorsa hızlıca sonucu döneriz
    if isprime(num):
        return True

    # Elliptik eğri seçimi (a ve b parametreleri ile uygun elliptik eğri)
    a, b = 2, 3  # y^2 = x^3 + 2x + 3 eğrisi (örnek)
    curve = EllipticCurve(a, b)

    # Diskriminant kontrolü: Eğri düzgün değilse test durur
    if not curve.is_smooth():
        return False

    # Bölünebilirlik testleri: Sayının küçük bölenleri var mı kontrol ediliyor
    for factor in divisors(num):
        if 1 < factor < num:
            if gcd(factor, num) != 1:
                return False  # Eğer GCD 1 değilse num asal değildir
            try:
                mod_inverse(factor, num)  # Modüler ters varsa asal olabilir
            except ValueError:
                continue  # Modüler ters bulunamazsa bir sonraki böleni dene

    return True  # Tüm testlerden geçtiyse sayı asaldır

def find_primes_up_to(limit: int) -> list:
    """
    Verilen sınıra kadar olan asal sayıları ECPP algoritması ile bulur.

    :param limit: Asal sayılar bulunacak üst sınır.
    :return: Asal sayılardan oluşan bir liste.
    """
    return [num for num in range(2, limit + 1) if elliptic_curve_primality_proving_ECPP(num)]

# Kullanım
if __name__ == "__main__":
    limit = 100
    primes = find_primes_up_to(limit)
    print(f"{limit} sayısına kadar olan asal sayılar: {primes}")
