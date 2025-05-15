import math

def ln_taylor(x, n_terms=1_000_00):
    if x <= 0:
        return "Doğal logaritma tanımsız!"
    
    # ln(x) değerini hesaplamak için logaritma dönüşümü
    y = (x - 1) / (x + 1)
    result = 0

    #Mercator serisi
    for n in range(1, n_terms * 2, 2):  # Sadece tek sayılar için
        result += (1 / n) * (y ** n)
    
    return 2 * result


def exp_approx(y, iterations=10):
    result = 1
    factorial = 1
    for i in range(1, iterations + 1):
        factorial *= i
        result += y ** i / factorial
    return result


def ln_newton(x, tolerance=1e-10, max_iter=100):
    if x <= 0:
        return "Doğal logaritma tanımsız!"

    y = x - 1  # Başlangıç tahmini
    for _ in range(max_iter):
        exp_y = exp_approx(y)
        y_next = y - (exp_y - x) / exp_y  # Newton-Raphson formülü
        if abs(y_next - y) < tolerance:
            return y_next
        y = y_next

    return y


result_math_log = math.log(100)
print(result_math_log)

x = 100
print(ln_taylor(x))

print(ln_newton(x))

math.e = 2
print(math.e)

if False:
    def custom_isclose(a, b, rel_tol=1e-9, abs_tol=0.0):
        # Toleransların negatif olmaması gerektiğini kontrol edelim
        if rel_tol < 0 or abs_tol < 0:
            raise ValueError("rel_tol and abs_tol must be non-negative")
        
        # Eğer a ve b eşitse, direkt True dönebiliriz (bu özel bir durumdur)
        if a == b:
            return True
        
        # Sonsuzluk durumlarını da ele almak gerekir
        if abs(a) == float('inf') and abs(b) == float('inf'):
            return a == b
        if abs(a) == float('-inf') and abs(b) == float('-inf'):
            return a == b

        # İki sayı arasındaki mutlak farkı hesapla
        diff = abs(a - b)
        
        # Göreceli toleransı hesapla: max(abs(a), abs(b)) * rel_tol
        rel_diff = rel_tol * max(abs(a), abs(b))
        
        # Mutlak fark, göreceli ve mutlak toleranslardan küçük mü?
        return diff <= max(rel_diff, abs_tol)

    # Örneklerle simülasyon
    print(custom_isclose(1e-10, 0.0, abs_tol=1e-9))  # True: abs_tol ile karşılaştırılır
    print(custom_isclose(1e-10, 0.0, abs_tol=1e-12))  # False: abs_tol çok küçük olduğu için fark büyük olur
    print(custom_isclose(1.0, 1.000000001, rel_tol=1e-9))  # True: Göreceli tolerans ile karşılaştırılır
    print(custom_isclose(float('inf'), float('inf')))  # True: Sonsuzluklar eşitse True döner
    print(custom_isclose(float('inf'), -float('inf')))  # False: Pozitif ve negatif sonsuzluklar eşit değildir


def inf_comp():
    a = float('inf')
    b = float('inf')
    c = float('-inf')

    # Pozitif sonsuzluklar eşittir
    print(a == b)  # True

    # Pozitif ve negatif sonsuzluklar eşit değildir
    print(a == c)  # False

    # Bir sayının sonsuz olup olmadığını kontrol edebiliriz
    print(a > b)  # True, sonsuz her zaman büyük bir değerdir

    import struct

    # Sonsuzluk (inf) değerini IEEE 754 formatında bitlerle gösterelim
    positive_inf = float('inf')
    negative_inf = float('-inf')

    # Çift hassasiyetli (64 bit) olarak sonsuzluk değerlerini paketleme
    positive_inf_bits = struct.unpack('>Q', struct.pack('>d', positive_inf))[0]
    negative_inf_bits = struct.unpack('>Q', struct.pack('>d', negative_inf))[0]

    # Bit dizisini ikilik (binary) formatta gösterme
    print(f"Pozitif sonsuzluk (inf) bitleri: {positive_inf_bits:064b}")
    print(f"Negatif sonsuzluk (-inf) bitleri: {negative_inf_bits:064b}")


def log_deneme():
    result_math_log = math.log(100)
    print(result_math_log)
    print((math.e) ** result_math_log)
    print(100 == (math.e) ** result_math_log)
    print(math.isclose(100, math.e ** result_math_log, rel_tol=1e-9))
    print(math.isclose(100, math.e ** result_math_log))

    # Üstel gösterimde sayılar
    a = 11e2   # 11 * 10^2
    b = 0.1e2  # 0.1 * 10^2
    c = -1e2   # -1 * 10^2
    d = 0e0    # 0 * 10^0

    # Sonuçları ekrana yazdırma
    print("11e2:", a, str(a))    # 1100.0
    print("0.1e2:", b)   # 10.0
    print("-1e2:", c)    # -100.0
    print("0e0:", d)     # 0.0