import sys
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

lock = threading.Lock()

def monitor_memory():
    global max_rss, max_vms

    def memory_task():
        while True:
            # Bellek kullanım bilgilerini al
            memory_info = process.memory_info()

            # Şu anki fiziksel ve sanal bellek kullanımı
            rss = memory_info.rss / (1024 ** 3)  # GB cinsinden
            vms = memory_info.vms / (1024 ** 3)  # GB cinsinden

            print(f"Current RSS: {rss:.5f} GB, VMS: {vms:.5f} GB")  # İzleme sırasında bellek kullanımını göster

            # Maksimum değerleri güncelle
            with lock:
                if rss > max_rss:
                    max_rss = rss
                if vms > max_vms:
                    max_vms = vms

            time.sleep(0.1)  # Belleği daha sık kontrol etmek için daha kısa süre

    # İş parçacığını başlat
    monitor_thread = threading.Thread(target=memory_task)
    monitor_thread.daemon = True  # Ana program bitince otomatik duracak
    monitor_thread.start()

    return monitor_thread

def compound():
    n = 10**5  # Daha hızlı test etmek için küçültüldü
    l = []
    print("Initial size of list:", sys.getsizeof(l))  # Başlangıç listesi boyutu
    l = [i for i in range(n)]
    print(f"Final list size (sys.getsizeof): {sys.getsizeof(l) / 1024 ** 3:.5f} GB")  # Bellek kullanımı (getsizeof)
    print(f"Expected memory usage: {(n * 28 + 56) / 1024 ** 3:.5f} GB")  # Beklenen bellek kullanımı

def main():
    tracemalloc.start()  # Bellek izlemeyi başlat

    # monitor_memory'i başlat
    monitor_thread = monitor_memory()

    # Compound fonksiyonunu çalıştır
    compound()

    # Monitor job'ı sonlandırmadan önce maksimum değerleri raporla
    with lock:
        print(f"Max Physical Memory (RSS): {max_rss:.5f} GB")
        print(f"Max Virtual Memory (VMS): {max_vms:.5f} GB")

    # Bellek izleme işlemini sonlandır ve raporla
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage: {current / (1024 ** 2):.5f} MB")
    print(f"Peak memory usage: {peak / (1024 ** 2):.5f} MB")

    tracemalloc.stop()  # Tracemalloc izlemeyi durdur

if __name__ == "__main__":
    main()
