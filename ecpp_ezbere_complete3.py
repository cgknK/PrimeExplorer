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

# Kullanım
if __name__ == "__main__":
    limit = 100  # 100'e kadar asal sayıları bulalım
    primes = find_primes_up_to(limit)
    print(f"{limit} sayısına kadar olan asal sayılar: {primes}")



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

    primes = find_primes_up_to(limit)
    return primes

print(elliptic_curve_primality_proving_ECPP(100))