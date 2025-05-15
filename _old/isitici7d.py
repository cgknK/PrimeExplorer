import concurrent.futures
import os
import time
import math
import logging
import psutil
import numpy as np
from threading import current_thread

# Global end_time değişkeni
end_time = None

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def cpu_loader():
    global end_time
    current = current_thread()
    try:
        p = psutil.Process(os.getpid())
        p.cpu_affinity([current.ident % os.cpu_count()])

        while time.time() < end_time:
            [math.exp(math.log(x**3.14) * 1.23) for x in range(1, 1001)]
        logging.info(f"Thread {current.name} tamamlandı.")
    except Exception as e:
        logging.error(f"Thread {current.name} hata: {e}")

def heat_cpu(duration):
    if duration <= 0:
        raise ValueError("Süre pozitif olmalıdır.")

    global end_time
    end_time = time.time() + duration
    num_workers = os.cpu_count()

    logging.info(f"CPU'yu {duration} saniye boyunca ısıtma başlatıldı.")

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(cpu_loader) for _ in range(num_workers)]

        cpu_usage_start = psutil.cpu_percent(interval=None)
        power_start = psutil.sensors_battery().power_plugged if psutil.sensors_battery() else None

        # Belirli aralıklarla CPU kullanımını ölç
        while time.time() < end_time:
            cpu_usage = psutil.cpu_percent(interval=1)  # 1 saniyelik aralıklarla ölçüm yap
            logging.info(f"Anlık CPU kullanımı: {cpu_usage}%")

        concurrent.futures.wait(futures)

        cpu_usage_end = psutil.cpu_percent(interval=None)
        power_end = psutil.sensors_battery().power_plugged if psutil.sensors_battery() else None

        logging.info(f"Başlangıç CPU kullanımı: {cpu_usage_start}%")
        logging.info(f"Son CPU kullanımı: {cpu_usage_end}%")
        logging.info(f"Başlangıç güç durumu: {'Bağlı' if power_start else 'Bağlı değil'}")
        logging.info(f"Son güç durumu: {'Bağlı' if power_end else 'Bağlı değil'}")

    logging.info("Tüm thread'ler tamamlandı.")

def optimize_memory_usage(size):
    try:
        array = np.random.random(size)
        logging.info(f"Bellek optimizasyonu: {size} boyutunda array oluşturuldu.")
        return array
    except MemoryError:
        logging.error("Bellek yetersizliği!")

if __name__ == "__main__":
    setup_logging()
    try:
        optimize_memory_usage(1000000)
        heat_cpu(60)
    except ValueError as e:
        logging.error(e)
