import sys
import math
import psutil
import time
import os
import tracemalloc


# Aktif çalışan process id'sini al
pid = os.getpid()

# Process hakkında bilgi al
process = psutil.Process(pid)

# Maksimum bellek değerlerini saklamak için değişkenler
max_rss = 0  # Maksimum fiziksel bellek (RSS)
max_vms = 0  # Maksimum sanal bellek (VMS)


def monitor_memory():
    global max_rss, max_vms

    # Bellek kullanım bilgilerini al
    memory_info = process.memory_info()

    # Şu anki fiziksel ve sanal bellek kullanımı
    rss = memory_info.rss / (1024 ** 3)  # GB cinsinden
    vms = memory_info.vms / (1024 ** 3)  # GB cinsinden

    print(f"Current RSS: {rss} GB, VMS: {vms} GB")  # İzleme sırasında bellek kullanımını göster

    # Maksimum değerleri güncelle
    if rss > max_rss:
        max_rss = rss
    if vms > max_vms:
        max_vms = vms


def primatif_1():
    print(sys.getsizeof(0))
    a = 0
    print(sys.getsizeof(a))
    print()
    print(sys.getsizeof(0.0))
    a = 0.0
    print(sys.getsizeof(a))
    print()
    print(sys.getsizeof(0e0))
    a = 0e0
    print(sys.getsizeof(a))
    pass


def primatif_2():
    print(sys.getsizeof(0))
    n = 2 ** 30 # 32 byte
    print(sys.getsizeof(n))
    n = 2 ** 30 - 1 # 24 byte
    print(sys.getsizeof(n))
    n = 2 ** 24
    print(sys.getsizeof(n))
    n = 2 ** 1000
    print(sys.getsizeof(n))
    pass


# 4*8 - 30 = 2 bit? bellek hizalaması mı atıl mı
def find_int_size_changes():
    last_size = sys.getsizeof(0)  # Başlangıç değeri olarak 0 için bellek boyutu
    current_size = last_size

    # Kaç tane boyut değişikliği olduğunu ve hangi değerlere geldiğini görmek için
    print(f"Initial size for 0: {last_size} bytes")
    
    i = 1
    while True:
        i *= 2
        current_size = sys.getsizeof(i)
        if current_size != last_size:
            print(f"Size changed at i = 2^{math.log(i)/math.log(2)}: {last_size} bytes -> {current_size} bytes")
            last_size = current_size

        if i > 2 ** 1_000:
            break


def compound():
    n = 10**9 // 2 // 100
    l = []
    print(sys.getsizeof(l))
    l = [i for i in range(n)]
    #######################################################################################################
    print(sys.getsizeof(l) / 1024**3, (n * 28 + 56) / 1024**3)# Nasıl daha düşük çıkıyor?
    #########################################################################################################
    print(sys.getsizeof(l[0]))
    print(sys.getsizeof(l[-1]))

    lst = [1, 2, 3, 4, 5]
    print("lst", sys.getsizeof(lst))  # Listenin referansının boyutu

    total_size = sys.getsizeof(l)  # Listenin kendisinin boyutu
    for elem in l:
        total_size += sys.getsizeof(elem)  # Her bir elemanın boyutunu ekle
        if elem == 499_000_000:
            print("500", sys.getsizeof(elem))

    #######################################################################################################
    print("total_size", total_size / 1024**3)  # Fakat program bu kadar bellek kullanmıyor? #sanal bellek olabilir.
    #######################################################################################################

    elem = lst[0]
    print(sys.getsizeof(elem))  # Belirli bir elemanın boyutu

    another_list = [1, 2, 3]
    lst = [another_list, 100]

    print(sys.getsizeof(lst[0]))  # İlk eleman olan 'another_list'in boyutu
    print(sys.getsizeof(lst[1]))  # İkinci eleman olan 100'ün boyutu


def main():
    tracemalloc.start()  # Bellek izlemeyi başlat

    # Bellek izlemeyi compound işlemi boyunca yap
    while True:
        monitor_memory()
        compound()
        break  # compound bittikten sonra belleği izlemeyi durdurmak için break kullanıyoruz

    # Bellek izleme işini durdur ve maksimum değerleri raporla
    print(f"Max Physical Memory (RSS): {max_rss} GB")
    print(f"Max Virtual Memory (VMS): {max_vms} GB")

    # Bellek izleme işlemini sonlandır ve raporla
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage: {current / (1024 ** 2)} MB")
    print(f"Peak memory usage: {peak / (1024 ** 2)} MB")


if __name__ == "__main__":
    main()