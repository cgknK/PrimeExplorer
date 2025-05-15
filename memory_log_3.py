import sys
import psutil
import time
import os
import tracemalloc
import threading

# Sabitler ve varsayılanlar
DEFAULT_INTERVAL = 0.5  # Bellek kontrolü aralığı (saniye)

class MemoryMonitor:
    """Bellek izleme işlemlerini yöneten sınıf."""
    
    def __init__(self, process_id: int, interval: float = DEFAULT_INTERVAL):
        """Bellek monitörü başlatır."""
        self.process = psutil.Process(process_id)
        self.max_rss = 0  # Maksimum fiziksel bellek (RSS)
        self.max_vms = 0  # Maksimum sanal bellek (VMS)
        self.interval = interval
        self.monitor_thread = None
        self.is_monitoring = False
        self.lock = threading.Lock()  # Thread-safe değişken erişimi için lock
    
    def _monitor_memory(self):
        """İç iş parçacığı tarafından çalıştırılan bellek izleme fonksiyonu."""
        while self.is_monitoring:
            memory_info = self.process.memory_info()
            rss = memory_info.rss / (1024 ** 3)  # GB cinsinden
            vms = memory_info.vms / (1024 ** 3)  # GB cinsinden

            print(f"Current RSS: {rss:.3f} GB, VMS: {vms:.3f} GB")

            # Maksimum değerleri güncelle
            with self.lock:
                self.max_rss = max(self.max_rss, rss)
                self.max_vms = max(self.max_vms, vms)

            time.sleep(self.interval)

    def start_monitoring(self):
        """Bellek izlemeyi iş parçacığında başlatır."""
        if self.is_monitoring:
            print("Memory monitoring is already running.")
            return

        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_memory, daemon=True)
        self.monitor_thread.start()
        print("Memory monitoring started.")

    def stop_monitoring(self):
        """Bellek izlemeyi durdurur."""
        if not self.is_monitoring:
            print("Memory monitoring is not running.")
            return

        self.is_monitoring = False
        self.monitor_thread.join()

        with self.lock:
            print(f"Max Physical Memory (RSS): {self.max_rss:.3f} GB")
            print(f"Max Virtual Memory (VMS): {self.max_vms:.3f} GB")

def test_memory_usage():
    """Bellek kullanımı testi için örnek bir işlem."""
    n = 10**5  # Büyük bir liste oluşturma
    lst = []
    print(f"Initial size of list: {sys.getsizeof(lst)} bytes")

    lst = [i for i in range(n)]
    total_size = sys.getsizeof(lst)  # Listenin kendisinin boyutu
    for elem in lst:
        total_size += sys.getsizeof(elem)  # Her bir elemanın boyutunu ekle
    print("->", n, total_size / 1024**2)
    print(f"Size of list after population: {sys.getsizeof(lst) / 1024**3:.3f} GB")
    print(f"Expected memory usage: {(n * 28 + sys.getsizeof(lst)) / 1024**3:.3f} GB")  # Tahmini kullanım

def main():
    """Ana fonksiyon."""
    tracemalloc.start()  # Bellek izlemeyi başlat

    # Process ID ve bellek monitörünü başlat
    process_id = os.getpid()
    monitor = MemoryMonitor(process_id)
    
    # Bellek izlemeyi başlat
    monitor.start_monitoring()

    # Bellek kullanımını test et
    test_memory_usage()

    # Bellek izlemeyi durdur ve raporla
    monitor.stop_monitoring()

    # Bellek izleme işlemini sonlandır ve raporla
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage: {current / (1024 ** 2):.2f} MB")
    print(f"Peak memory usage: {peak / (1024 ** 2):.2f} MB")
    
    # Tracemalloc izlemeyi durdur
    tracemalloc.stop()

if __name__ == "__main__":
    main()
