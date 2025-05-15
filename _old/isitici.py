import threading
import os  # os modülünü içe aktarın
import time

def heat_cpu(duration):
    def islemci_yukleyici():
        # Belirli bir süre boyunca çalışacak
        end_time = time.time() + duration
        while time.time() < end_time:
            pass

    thread_listesi = []
    for i in range(os.cpu_count()):  # os.cpu_count() kullanın
        thread = threading.Thread(target=islemci_yukleyici)
        thread_listesi.append(thread)
        thread.start()

    # Tüm thread'lerin bitmesini bekleyelim
    for thread in thread_listesi:
        thread.join()

# 60 saniye boyunca CPU'yu ısıt
heat_cpu(60)
