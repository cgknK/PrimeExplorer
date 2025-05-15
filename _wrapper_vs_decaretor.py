import time

def cpu_time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.process_time()
        
        result = func(*args, **kwargs)  # Orijinal fonksiyon çağrılıyor
        
        end_time = time.process_time()
        cpu_time_used = end_time - start_time
        print(f"CPU time used by {func.__name__}: {cpu_time_used:.6f} seconds")
        
        return result
    return wrapper

@cpu_time_decorator
def slow_function(n):
    time.sleep(n//10)  # 2 saniye bekleyen bir fonksiyon

# slow_function'u çalıştırıyoruz, zaman otomatik olarak ölçülecek
slow_function(10)


try:
    def slow_function2(n):
        time.sleep(n//10)  # 2 saniye bekleyen bir fonksiyon

    def run_with_timing(func):
        start_time = time.process_time()
        
        result = func()  # Orijinal fonksiyonu burada çağırıyoruz
        
        end_time = time.process_time()
        cpu_time_used = end_time - start_time
        print(f"CPU time used by {func.__name__}: {cpu_time_used:.6f} seconds")
        
        return result

    # slow_function'u zaman ölçümü ile çalıştırıyoruz
    run_with_timing(slow_function2(10))
except Exception as e:
    print(e)
print()

###############################

import time

def cpu_time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.process_time()
        
        result = func(*args, **kwargs)  # Orijinal fonksiyon çağrılıyor
        
        end_time = time.process_time()
        cpu_time_used = end_time - start_time
        print(f"CPU time used by {func.__name__}: {cpu_time_used:.6f} seconds")
        
        return result
    return wrapper

@cpu_time_decorator
def add(x, y):
    time.sleep(1)  # 1 saniye bekleyen bir fonksiyon
    return x + y

# add fonksiyonunu çalıştırıyoruz, zaman otomatik olarak ölçülecek
result = add(5, 7)
print(f"Result: {result}")
print()
#-------------------------------------------------------------------------------

import time

def run_with_timing(func, *args, **kwargs):
    start_time = time.process_time()
    
    result = func(*args, **kwargs)  # Orijinal fonksiyonu burada çağırıyoruz
    
    end_time = time.process_time()
    cpu_time_used = end_time - start_time
    print(f"CPU time used by {func.__name__}: {cpu_time_used:.6f} seconds")
    
    return result

def add(x, y):
    time.sleep(1)  # 1 saniye bekleyen bir fonksiyon
    return x + y

# add fonksiyonunu zaman ölçümü ile çalıştırıyoruz
result = run_with_timing(add, 5, 7)  # Argümanları burada geçiyoruz
print(f"Result: {result}")
print("\n" * 5)


###############

import time

def cpu_time_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Original function name: {func.__name__}")
        start_time = time.process_time()
        
        result = func(*args, **kwargs)  # Orijinal fonksiyon çağrılıyor
        
        end_time = time.process_time()
        cpu_time_used = end_time - start_time
        print(f"CPU time used by {func.__name__}: {cpu_time_used:.6f} seconds")
        
        return result
    return wrapper


def add(x, y):
    time.sleep(1)  # 1 saniye bekleyen bir fonksiyon
    return x + y

deneme = cpu_time_decorator(add)

# add fonksiyonunu çalıştırıyoruz, zaman otomatik olarak ölçülecek
result = deneme(1, 2)#ddd(5, 7)
print(f"Result: {result}")
print()