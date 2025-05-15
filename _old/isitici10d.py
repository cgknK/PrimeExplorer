import os
import time
import math
import logging
import psutil
from multiprocessing import Process, current_process

# Global end_time değişkeni
end_time = None

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def cpu_loader(load, duration, core_id):
    global end_time
    end_time = time.time() + duration
    current = current_process()
    try:
        p = psutil.Process(os.getpid())
        p.cpu_affinity([core_id])  # Her çekirdek için affinity ayarı

        if load > 0:  # Yük 0'dan büyük olmalı
            while time.time() < end_time:
                for _ in range(load):
                    for _ in range(1000):
                        math.exp(math.log(1234.5678))
        logging.info(f"Process {current.name} (Core {core_id}) tamamlandı.")
    except Exception as e:
        logging.error(f"Process {current.name} (Core {core_id}) hata: {e}")

def monitor_cpu(interval, duration):
    global end_time
    end_time = time.time() + duration
    while time.time() < end_time:
        cpu_usage = psutil.cpu_percent(interval=interval, percpu=True)
        logging.info(f"Anlık CPU kullanımı: {cpu_usage}")

def heat_cpu(duration, load_per_core):
    if duration <= 0:
        raise ValueError("Süre pozitif olmalıdır.")
    if any(load < 0 for load in load_per_core):  # Negatif yük kontrolü
        raise ValueError("Yük negatif olmamalıdır.")

    num_workers = os.cpu_count()

    if len(load_per_core) != num_workers:
        raise ValueError(f"Yük listesi {num_workers} çekirdek için belirlenmelidir.")

    logging.info(f"CPU'yu {duration} saniye boyunca çekirdek başına yük ({load_per_core}) ile ısıtma başlatıldı.")

    monitor_thread = Process(target=monitor_cpu, args=(1, duration))
    monitor_thread.start()

    processes = []
    for i in range(num_workers):
        p = Process(target=cpu_loader, args=(load_per_core[i], duration, i))
        p.start()
        processes.append(p)

    cpu_usage_start = psutil.cpu_percent(interval=None)
    power_start = psutil.sensors_battery().power_plugged if psutil.sensors_battery() else None

    try:
        for p in processes:
            p.join()
    except KeyboardInterrupt:
        logging.warning("Kullanıcı tarafından kesildi.")
        for p in processes:
            p.terminate()

    monitor_thread.join()

    cpu_usage_end = psutil.cpu_percent(interval=None)
    power_end = psutil.sensors_battery().power_plugged if psutil.sensors_battery() else None

    logging.info(f"Başlangıç CPU kullanımı: {cpu_usage_start}%")
    logging.info(f"Son CPU kullanımı: {cpu_usage_end}%")
    logging.info(f"Başlangıç güç durumu: {'Bağlı' if power_start else 'Bağlı değil'}")
    logging.info(f"Son güç durumu: {'Bağlı' if power_end else 'Bağlı değil'}")

    logging.info("Tüm process'ler tamamlandı.")

if __name__ == "__main__":
    setup_logging()
    try:
        # Her çekirdek için ayrı yük belirtin
        # Örneğin, 4 çekirdek varsa ve hepsini %100 yük ile çalıştırmak isterseniz
        loads = [1000, 1, 0, 0]
        heat_cpu(60, loads)
    except ValueError as e:
        logging.error(e)
