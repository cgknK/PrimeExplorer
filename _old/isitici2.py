import threading
import os
import time

# Global end_time değişkeni
end_time = None

def islemci_yukleyici():
    # Belirli bir süre boyunca çalışacak
    global end_time
    while time.time() < end_time:
        [(x**2)/((x+1)**1.15) for x in range(1000)] # pass yerine

def heat_cpu(duration):
    global end_time
    end_time = time.time() + duration

    # Thread oluşturma ve başlatma
    thread_listesi = [threading.Thread(target=islemci_yukleyici) for _ in range(os.cpu_count())]
    for thread in thread_listesi:
        thread.start()

    # Tüm thread'lerin bitmesini bekleyelim
    for thread in thread_listesi:
        thread.join()

if __name__ == "__main__":
    # 60 saniye boyunca CPU'yu ısıt
    heat_cpu(60)
