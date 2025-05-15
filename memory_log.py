import sys
import math
import psutil
import time
import os
import tracemalloc
import threading

# Aktif çalışan process id'sini al
pid = os.getpid()

# Process hakkında bilgi al
process = psutil.Process(pid)

# Maksimum bellek değerlerini saklamak için değişkenler
max_rss = 0  # Maksimum fiziksel bellek (RSS)
max_vms = 0  # Maksimum sanal bellek (VMS)

# Thread-safe erişim sağlamak için bir kilit (lock) oluştur
lock = threading.Lock()

def monitor_memory():
    global max_rss, max_vms
    while True:
        # Bellek kullanım bilgilerini al
        memory_info = process.memory_info()

        # Şu anki fiziksel ve sanal bellek kullanımı
        rss = memory_info.rss / (1024 ** 3)  # GB cinsinden
        vms = memory_info.vms / (1024 ** 3)  # GB cinsinden

        print(f"Current RSS: {rss} GB, VMS: {vms} GB")  # İzleme sırasında bellek kullanımını göster

        # Kilit ile güvenli bir şekilde maksimum değerleri güncelle
        with lock:
            if rss > max_rss:
                max_rss = rss
            if vms > max_vms:
                max_vms = vms

        time.sleep(0.5)  # Belleği düzenli aralıklarla kontrol etmek için uyut

def compound():
    n = 10**5  # Daha hızlı test etmek için küçülttüm
    l = []
    print(sys.getsizeof(l))
    l = [i for i in range(n)]
    print(sys.getsizeof(l) / 1024**3, (n * 28 + 56) / 1024**3)  # Bellek kullanımı

def main():
    tracemalloc.start()  # Bellek izlemeyi başlat

    # Bellek izlemeyi ayrı bir iş parçacığı olarak başlat
    monitor_thread = threading.Thread(target=monitor_memory)
    monitor_thread.daemon = True  # Ana program bitince otomatik duracak
    monitor_thread.start()

    # Compound fonksiyonunu çalıştır
    compound()

    # Bellek izleme işini durdur ve maksimum değerleri raporla
    print(f"Max Physical Memory (RSS): {max_rss} GB")
    print(f"Max Virtual Memory (VMS): {max_vms} GB")

    # Bellek izleme işlemini sonlandır ve raporla
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage: {current / (1024 ** 2)} MB")
    print(f"Peak memory usage: {peak / (1024 ** 2)} MB")

    tracemalloc.stop()  # Tracemalloc izlemeyi durdur

if __name__ == "__main__":
    main()
