"""
GCD (En Büyük Ortak Bölen) algoritmaları, iki veya daha fazla sayının ortak bölenlerinin en büyüğünü bulmak için kullanılır. En bilinen ve yaygın kullanılan GCD algoritmaları şunlardır:

### 1. **Öklid Algoritması (Euclidean Algorithm)**

En temel ve yaygın kullanılan GCD algoritmasıdır. **Öklid algoritması**, iki sayının en büyük ortak bölenini bulmak için modüler aritmetiğe dayalıdır. Temeli şudur: İki sayı \( a \) ve \( b \) verildiğinde, eğer \( a \) büyükse \( gcd(a, b) = gcd(b, a \mod b) \) geçerlidir. Bu işlemi tekrarlayarak sonunda bir sayının diğerine bölündüğü noktaya gelinir ve bu noktada kalan sıfır olduğunda, bölen sayı GCD'dir.

#### Adımlar:
- \( gcd(a, b) = gcd(b, a \mod b) \) kullanılarak tekrarlanır.
- \( a \mod b = 0 \) olduğunda GCD, \( b \)'dir.

#### Örnek:
\( a = 48 \), \( b = 18 \)
- \( 48 \mod 18 = 12 \)
- \( 18 \mod 12 = 6 \)
- \( 12 \mod 6 = 0 \)

Sonuç: \( gcd(48, 18) = 6 \).

Bu algoritmanın zaman karmaşıklığı, iki sayının büyüklüğü ile doğru orantılıdır. Zaman karmaşıklığı genellikle \( O(\log(\min(a,b))) \)'dir.

### 2. **Genişletilmiş Öklid Algoritması (Extended Euclidean Algorithm)**

**Genişletilmiş Öklid algoritması**, yalnızca GCD'yi bulmakla kalmaz, aynı zamanda **Bézout kimlikleri** adı verilen \( ax + by = gcd(a, b) \) şeklindeki lineer denklemi sağlayan \( x \) ve \( y \) katsayılarını da bulur. Bu denklemin çözümleri, genellikle **modüler ters** veya **Diofant denklemleri** çözümlerinde kullanılır.

#### Adımlar:
1. Normal Öklid algoritmasını çalıştırarak GCD bulunur.
2. GCD geri takip edilerek \( x \) ve \( y \) katsayıları hesaplanır.

#### Örnek:
\( a = 30 \), \( b = 20 \)
- \( gcd(30, 20) = 10 \)
- Denklemi çözmek için: \( 30x + 20y = 10 \)
- Sonuçta \( x = 1 \), \( y = -1 \) bulunur, yani \( 30(1) + 20(-1) = 10 \).

Bu yöntem genellikle **modüler aritmetik** ve **kriptografide** (örneğin RSA algoritmasında) kullanılır.

### 3. **Stein Algoritması (Binary GCD Algoritması)**

**Stein algoritması**, modüler işlemleri ortadan kaldırarak sadece bit manipülasyonlarıyla GCD hesaplayan bir yöntemdir. Sayılar üzerinde sadece bölme ve çarpma işlemleri yerine, **bit kaydırma** ve **çıkarma** işlemleri kullanılır. Bu nedenle bu algoritma, bilgisayar mimarisinde daha verimli olabilir.

#### Adımlar:
1. Eğer \( a \) ve \( b \) ikisi de çiftse, \( gcd(a, b) = 2 \times gcd(a/2, b/2) \).
2. Eğer \( a \) çift ve \( b \) tekse, \( gcd(a, b) = gcd(a/2, b) \).
3. Eğer \( a \) tek ve \( b \) çiftse, \( gcd(a, b) = gcd(a, b/2) \).
4. Eğer her ikisi de tekse, \( gcd(a, b) = gcd(|a - b|, \min(a, b)) \).

Bu işlemler, sayılar bit düzeyinde işlenerek yapılır ve oldukça verimlidir.

#### Örnek:
\( a = 48 \), \( b = 18 \)
- İkisi de çift, bu yüzden: \( gcd(48, 18) = 2 \times gcd(24, 9) \)
- Şimdi \( a = 24 \), \( b = 9 \)
- \( a \) çift, \( b \) tek, bu yüzden: \( gcd(24, 9) = gcd(12, 9) \)
- Aynı şekilde devam edilerek GCD hesaplanır.

Stein algoritmasının zaman karmaşıklığı, Öklid algoritmasıyla benzerdir, ancak bit manipülasyonları kullandığı için bazı durumlarda daha hızlı olabilir.

### 4. **Brute Force (Zorlayıcı Yöntem)**

Bu yöntem en basit olanıdır ancak büyük sayılarla çalışırken verimsizdir. İki sayının GCD'sini bulmak için, bu sayıları bölen tüm pozitif sayılar hesaplanır ve ortak olan en büyük bölen seçilir.

#### Adımlar:
1. İki sayının ortak bölenleri bulunur.
2. Ortak bölenler arasındaki en büyük sayı GCD'dir.

#### Örnek:
\( a = 48 \), \( b = 18 \)
- 48'in bölenleri: \( 1, 2, 3, 4, 6, 8, 12, 16, 24, 48 \)
- 18'in bölenleri: \( 1, 2, 3, 6, 9, 18 \)
- Ortak bölenler: \( 1, 2, 3, 6 \)
- Sonuç: GCD \( 6 \)'dır.

Bu yöntem \( O(\min(a, b)) \) zaman karmaşıklığına sahiptir ve büyük sayılar için pratik değildir.

### 5. **Recursive GCD (Özyinelemeli GCD)**

Öklid algoritması, özyinelemeli (recursive) olarak da uygulanabilir. Bu yaklaşım, GCD'yi özyinelemeli bir fonksiyonla bulur. İşleyişi aynıdır, ancak daha basit bir özyineleme yapısına sahiptir.

#### Adımlar:
- \( gcd(a, b) \) özyinelemeli olarak şu şekilde ifade edilir:
  - Eğer \( b = 0 \) ise, GCD \( a \)'dır.
  - Aksi takdirde \( gcd(b, a \mod b) \)'yi çağır.

#### Örnek:
```python
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

print(gcd(48, 18))  # Sonuç: 6
```

### 6. **Parallel GCD Algoritmaları**

Modern hesaplamalarda paralel işlemciler kullanarak GCD hesaplamaları daha hızlı yapılabilir. Paralel GCD algoritmaları, genellikle Stein algoritmasına dayanır ve sayıları daha küçük parçalara ayırarak hesaplamayı paralel olarak gerçekleştirir.

#### Örnek:
- Sayılar eşit parçalara bölünür ve her parça üzerinde GCD hesaplanır.
- Bu kısmi sonuçlar birleştirilerek son GCD elde edilir.

Paralel algoritmalar genellikle büyük veri kümeleri ve paralel işlemciye sahip sistemlerde daha verimli çalışır.

---

### Sonuç:
En yaygın GCD algoritması Öklid algoritmasıdır ve genişletilmiş versiyonu ile daha fazla kullanım alanına sahiptir. Stein algoritması, bit manipülasyonları kullanarak GCD hesaplama sürecini hızlandırabilir. Brute force gibi daha basit yöntemler ise küçük sayılar için uygundur ancak büyük sayılarla verimsiz hale gelir.
"""



#Pollard Rho algoritması
import math


def pollard_rho_hatali(num):
    num = int(num)
    if num == 1:#sentinel
        return 1

    temp = []#rho
    x_base = 2
    temp.append(x_base)
    while True:
        f_x = x_base ** 2 + 1
        temp.append(f_x)
        x_base = f_x

        if x_base in temp:
            break

    delta_x_y = abs(temp[-2] - temp[-1])
    if  delta_x_y > 0:
        result = math.gcd(delta_x_y, num)
        return [pollard_rho_hatali(num / result), result]
    else:
        return [result, num / result]


#print(pollard_rho_hatali(6))


def extended_euclidean():
    pass


from functools import reduce

# Öklid algoritması ile iki sayının GCD'sini hesaplama
def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)

# Birden fazla argümanı destekleyen GCD fonksiyonu
def gcd_multiple(*args):
    if not args:  # Argüman yoksa 0 döner
        return 0
    return reduce(gcd, args)

# Örnek kullanım
print(gcd_multiple(48, 64, 16))  # Çıktı: 16
print(gcd_multiple(20, 50, 30))  # Çıktı: 10
print(gcd_multiple(0, 0))        # Çıktı: 0
print(gcd_multiple())            # Çıktı: 0
print(gcd_multiple(2, 3, 5, 7))
