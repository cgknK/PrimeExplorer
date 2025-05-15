import concurrent.futures
import os
import time
import math

# Global end_time değişkeni
end_time = None

def cpu_loader():
    # Belirli bir süre boyunca çalışacak
    global end_time
    while time.time() < end_time:
        [math.sqrt(x) for x in range(1000)] # Daha hızlı matematiksel işlem

def heat_cpu(duration):
    global end_time
    end_time = time.time() + duration

    # Thread oluşturma ve başlatma
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(cpu_loader) for _ in range(os.cpu_count())]

        # Tüm thread'lerin bitmesini bekleyelim
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    # 60 saniye boyunca CPU'yu ısıt
    heat_cpu(60)
