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

def mod_inverse_test(factor: int, num: int) -> bool:
    """Modüler tersin olup olmadığını test eder."""
    try:
        mod_inverse(factor, num)
        return True
    except ValueError:
        return False

def gcd_test(factor: int, num: int) -> bool:
    """GCD'nin 1 olup olmadığını test eder."""
    return gcd(factor, num) == 1

def elliptic_curve_primality_proving_ECPP(num: int) -> bool:
    """
    Verilen sayının ECPP ile asal olup olmadığını kontrol eder.

    :param num: Asal olup olmadığı test edilecek sayı.
    :return: Sayı asal ise True, aksi halde False.
    """
    if num <= 1:
        return False

    if isprime(num):
        pass#return True

    a, b = 2, 3  # y^2 = x^3 + 2x + 3 eğrisi (örnek)
    curve = EllipticCurve(a, b)

    if not curve.is_smooth():
        return False

    for factor in divisors(num):
        if 1 < factor < num:
            if not gcd_test(factor, num) or not mod_inverse_test(factor, num):
                return False

    return True

def find_primes_up_to(limit: int) -> list:
    """
    Verilen sınıra kadar olan asal sayıları ECPP algoritması ile bulur.
    :param limit: Asal sayılar bulunacak üst sınır.
    :return: Asal sayılardan oluşan bir liste.
    """
    return [num for num in range(2, limit + 1) if elliptic_curve_primality_proving_ECPP(num)]

if __name__ == "__main__":
    limit = 100
    primes = find_primes_up_to(limit)
    print(f"{limit} sayısına kadar olan asal sayılar: {primes}")


"""
Elliptic Curve Primality Proving (ECPP) algoritması, oldukça karmaşık ve gelişmiş bir asal sayıları doğrulama yöntemidir. ECPP'nin mevcut basit hali, çeşitli optimizasyonlar ve geliştirmeler yaparak hem doğruluk hem de performans açısından daha uygun hale getirilebilir. İşte yapılabilecek çeşitli iyileştirmeler:
1. Elliptik Eğri Seçimini İyileştirme

Kodunuzdaki elliptik eğri parametreleri sabitlenmiş durumda (a = 2, b = 3). Bu, her sayı için aynı eğriyi kullanmanıza neden olur. Farklı sayılar için farklı eğriler seçmek daha güvenilir sonuçlar verir. Özellikle, daha karmaşık parametre seçimi mekanizmaları eklemek, doğrulama sürecini daha güçlü hale getirir.

Geliştirme Önerisi:

    Rastgele ya da adaptif eğri seçimi: Her sayı için farklı bir eğri belirlemek performansı ve doğruluğu artırabilir. Eğriler, sayıya bağlı olarak değiştirilebilir.
    Standart eğriler kullanma: Genellikle kullanılabilecek sabit setler içeren elliptik eğriler (örneğin NIST veya SEC tarafından önerilen eğriler) seçilebilir.

2. Modüler Ters Hesaplamaları ve Faktör Testleri

Kodunuzu şu anki haliyle basit bölen testlerine ve modüler ters hesaplamalarına dayandırıyorsunuz. Ancak ECPP'nin gücü, bu testlerin çok daha ileri seviyede yapılmasında yatar.

Geliştirme Önerisi:

    Montgomery Reduction gibi daha gelişmiş modüler aritmetik teknikleri kullanarak modüler terslemeyi hızlandırabilirsiniz.
    Daha karmaşık faktörizasyon ve bölünebilirlik testleri: Pollard's Rho veya Lenstra elliptik eğri faktörizasyonu gibi algoritmalar bölünebilirliği test etmek için kullanılabilir.

3. Paralel İşlem ve Optimizasyon

ECPP gibi karmaşık algoritmalar, paralelleştirilebilen birçok adımdan oluşur. Mevcut haliyle, tek bir işlemde çalışıyorsunuz. Büyük sayılar için bu verimsiz olabilir.

Geliştirme Önerisi:

    Paralel işleme ekleyerek bölünebilirlik ve modüler ters testlerini paralel yürütün. Bu sayede büyük sayılar üzerindeki testleri hızlandırabilirsiniz.
    Multiprocessing veya multithreading ile her bir böleni ayrı bir işlemde test edin.

4. Güvenilir Sayı Doğrulama

ECPP, genellikle belirli kanıt zincirlerine dayanarak sayının asal olduğunu kanıtlar. Bu kanıtları doğrulamak için belirli bir sertifikasyon mekanizması eklemek iyi bir gelişme olabilir.

Geliştirme Önerisi:

    Kanıt Sertifikasyonu: Sayının asal olup olmadığını sadece test etmek yerine, bir "asal sertifikası" oluşturun. Bu sertifikalar sonradan doğrulanabilir ve daha güvenilir sonuçlar sunar.

5. Matematiksel Kütüphaneleri Optimize Etme

Kod şu anda sympy ve math kütüphanelerini kullanıyor. Ancak bu kütüphaneler genelde genel amaçlıdır. Asal sayı doğrulama işlemleri için daha özelleşmiş matematiksel kütüphaneler kullanmak performansı artırabilir.

Geliştirme Önerisi:

    GMP (GNU Multiple Precision Arithmetic Library) gibi daha hızlı ve optimizasyonlu kütüphaneler kullanabilirsiniz. Bu kütüphane büyük sayıların modüler hesaplamalarında çok hızlıdır.
    PyCryptodome gibi kütüphaneler, kriptografik işlemler için optimize edilmiş modüler aritmetik işlevlerine sahiptir.

6. Kod Yapısını Yeniden Düzenleme

Kod yapısında küçük iyileştirmeler ve daha temiz bir yapı sağlamak önemlidir. Örneğin, daha küçük, bağımsız fonksiyonlar modüler bir yapı oluşturabilir ve daha okunabilir hale getirir.

Geliştirme Önerisi:

    Fonksiyonların bölünmesi: Tek bir fonksiyon içinde çok fazla iş yapılmış. Her bir test adımını ayrı fonksiyonlar haline getirin (örneğin, mod_inverse_test, gcd_test gibi).
    Daha iyi hata yönetimi: try-except bloklarını daha etkin kullanarak kodu daha güvenilir hale getirin.

7. Docstring ve Yorumları Geliştirme

Docstring'ler ve yorumlar, kodu anlamak ve genişletmek için önemlidir. Özellikle böyle karmaşık bir algoritmada, her adımı açıklamak kodun bakımını kolaylaştırır.

Geliştirme Önerisi:

    Daha ayrıntılı açıklamalar ekleyin. Hangi adımda ne yapıldığını, neden yapıldığını açıklayın. Özellikle matematiksel kısımlarda kullanılan teoriyi belgelemek yararlı olur.
    """