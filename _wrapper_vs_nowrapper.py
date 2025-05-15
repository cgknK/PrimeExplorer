from concurrent.futures import ProcessPoolExecutor
import time

# Basit bir işlev
def square(x):
    return x * x

# Paralel işlem
def main_no_wrapper():
    numbers = [1, 2, 3, 4, 5]
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(square, numbers))  # Doğrudan square fonksiyonunu çağırıyoruz
    print(results)

if __name__ == '__main__':
    main_no_wrapper()


# Basit bir işlev
def square(x):
    return x * x

# Wrapper fonksiyonu
def run_square(args):
    return square(*args)  # Args tuple'ını açarak kullanıyoruz

# Paralel işlem
def main_with_wrapper():
    numbers = [(1,), (2,), (3,), (4,), (5,)]  # Her sayı bir tuple içinde
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(run_square, numbers))  # Wrapper fonksiyonunu kullanıyoruz
    print(results)

if __name__ == '__main__':
    main_with_wrapper()


try:
    from concurrent.futures import ProcessPoolExecutor

    # İki argümanı toplayan basit bir işlev
    def add(x, y):
        return x + y

    # Paralel işlem (wrapper kullanılmadan)
    def main_no_wrapper():
        numbers = [1, 2, 3, 4, 5]
        # Burada her bir çift argümanı temsil eden bir liste oluşturmalıyız
        pairs = [(num, num + 1) for num in numbers]  # Örnek çiftler: (1, 2), (2, 3), ...
        print("   ", pairs)

        # Bu kısım çalışmayacak çünkü add iki argüman alıyor
        with ProcessPoolExecutor() as executor:
            results = list(executor.map(add, pairs))  # Hata verecek
        print(results)

    if __name__ == '__main__':
        main_no_wrapper()
except Exception as e:  # Hataları yakalamak için doğru except kullanımı
        print(f"Hata: {e}")


from concurrent.futures import ProcessPoolExecutor

# İki argümanı toplayan basit bir işlev
def add(x, y):
    return x + y

# Wrapper fonksiyonu
def run_add(args):
    return add(*args)  # Args tuple'ını açarak kullanıyoruz

# Paralel işlem (wrapper kullanarak)
def main_with_wrapper():
    numbers = [1, 2, 3, 4, 5]
    # Her çift argümanı temsil eden bir liste oluşturuyoruz
    pairs = [(num, num + 1) for num in numbers]  # Örnek çiftler: (1, 2), (2, 3), ...

    with ProcessPoolExecutor() as executor:
        results = list(executor.map(run_add, pairs))  # Wrapper fonksiyonunu kullanıyoruz
    print(results)

if __name__ == '__main__':
    main_with_wrapper()
