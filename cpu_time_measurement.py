import os
import time
from multiprocessing import Process, Pool
import psutil

# 1. Yaklaşım: multiprocessing modülü ve os.times() ile CPU Zamanını Ölçmek
def worker_1():
    # Simülasyon için işlem süresi ekleyelim
    a = 0
    for _ in range(10**7):
        a /= _ * _ + 1

def measure_multiprocessing_os_times():
    start = os.times()  # Başlangıç CPU zamanını al
    processes = []

    for _ in range(4):  # 4 worker
        p = Process(target=worker_1)
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    end = os.times()  # Bitiş CPU zamanını al

    user_time = end.user - start.user
    system_time = end.system - start.system

    print(f"Multiprocessing os.times() - Kullanıcı Zamanı: {user_time} saniye")
    print(f"Multiprocessing os.times() - Sistem Zamanı: {system_time} saniye")

# 2. Yaklaşım: multiprocessing.Pool kullanarak CPU zamanlarını ölçmek
def worker_2(n):
    # Simülasyon için işlem süresi ekleyelim
    a = 0
    for _ in range(n):
        a /= _ * _ + 1

def measure_multiprocessing_pool():
    n = 10**7
    start = os.times()  # Başlangıç CPU zamanını al

    with Pool(4) as p:
        p.map(worker_2, [n, n, n, n])

    end = os.times()  # Bitiş CPU zamanını al

    user_time = end.user - start.user
    system_time = end.system - start.system

    print(f"Multiprocessing Pool - Kullanıcı Zamanı: {user_time} saniye")
    print(f"Multiprocessing Pool - Sistem Zamanı: {system_time} saniye")

# 3. Yaklaşım: psutil ile CPU Zamanını İzleme
def worker_3():
    # İşlem simülasyonu
    a = 0
    for _ in range(10**7):
        a /= _ * _ + 1

def measure_with_psutil():
    start_time = time.time()
    processes = []
    for _ in range(4):
        p = Process(target=worker_3)
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    end_time = time.time()
    print(f"psutil - Toplam Gerçek Zaman: {end_time - start_time} saniye")

    # CPU sürelerini psutil ile ölçmek
    process = psutil.Process()
    cpu_times = process.cpu_times()
    print(f"psutil - Kullanıcı Zamanı: {cpu_times.user} saniye")
    print(f"psutil - Sistem Zamanı: {cpu_times.system} saniye")

if __name__ == '__main__':
    print("1. Yaklaşım: multiprocessing ve os.times()")
    measure_multiprocessing_os_times()

    print("\n2. Yaklaşım: multiprocessing.Pool ile")
    measure_multiprocessing_pool()

    print("\n3. Yaklaşım: psutil ile CPU Zamanı")
    measure_with_psutil()
