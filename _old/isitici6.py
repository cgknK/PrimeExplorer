# Gerekli modülleri içe aktar
import concurrent.futures
import os
import time
import math
import logging
import psutil  # Sistem ve CPU performans ölçümleri için kullanılacak modül
import numpy as np  # Bellek yönetimi ve rastgele sayı üretimi için kullanılacak modül
from threading import current_thread  # Mevcut thread'in bilgilerine erişim için kullanılacak modül

# İşlemlerin bitiş zamanını global olarak tanımla
end_time = None

# Loglama yapılandırmasını ayarlayan fonksiyon
def setup_logging():
    # Log seviyesini INFO olarak ayarla ve log mesajlarının formatını belirle
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# CPU'yu yükleyecek olan fonksiyon
def cpu_loader():
    # Global değişkeni kullanmak için global anahtar kelimesi
    global end_time
    # Mevcut thread'in bilgisini al
    current = current_thread()
    # İşlemciye bağlama işlemi için psutil.Process kullan
    p = psutil.Process(os.getpid())
    # Mevcut thread'i işlemcinin belirli bir çekirdeğine bağla
    p.cpu_affinity([current.ident % os.cpu_count()])

    # Belirlenen bitiş zamanına kadar döngüyü sürdür
    while time.time() < end_time:
        # Yoğun matematiksel işlem yapan bir list comprehension
        [math.exp(math.log(x**3.14) * 1.23) for x in range(1, 1001)]
    # Thread'in tamamlandığını logla
    logging.info(f"Thread {current.name} tamamlandı.")

# CPU'yu belirli bir süre boyunca yükleyecek olan fonksiyon
def heat_cpu(duration):
    # Sürenin pozitif olup olmadığını kontrol et, değilse hata fırlat
    if duration <= 0:
        raise ValueError("Süre pozitif olmalıdır.")

    # Global 'end_time' değişkenini ayarla
    global end_time
    end_time = time.time() + duration
    # Sistemdeki CPU çekirdek sayısını al
    num_workers = os.cpu_count()

    # Isıtma işleminin başladığını logla
    logging.info(f"CPU'yu {duration} saniye boyunca ısıtma başlatıldı.")

    # ThreadPoolExecutor ile thread havuzu oluştur ve yönet
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        # Her bir CPU çekirdeği için bir thread oluştur ve cpu_loader fonksiyonunu çalıştır
        futures = [executor.submit(cpu_loader) for _ in range(num_workers)]

        # CPU performans ve enerji tüketimini izleme
        cpu_usage_start = psutil.cpu_percent(interval=None)
        power_start = psutil.sensors_battery().power_plugged if psutil.sensors_battery() else None

        # Tüm thread'lerin bitmesini bekleyelim
        concurrent.futures.wait(futures)

        # CPU kullanımı ve güç durumunu logla
        cpu_usage_end = psutil.cpu_percent(interval=None)
        power_end = psutil.sensors_battery().power_plugged if psutil.sensors_battery() else None

        logging.info(f"Başlangıç CPU kullanımı: {cpu_usage_start}%")
        logging.info(f"Son CPU kullanımı: {cpu_usage_end}%")
        logging.info(f"Başlangıç güç durumu: {'Bağlı' if power_start else 'Bağlı değil'}")
        logging.info(f"Son güç durumu: {'Bağlı' if power_end else 'Bağlı değil'}")

    # Tüm thread'lerin tamamlandığını logla
    logging.info("Tüm thread'ler tamamlandı.")

# Bellek kullanımını optimize eden fonksiyon
def optimize_memory_usage(size):
    # Belirtilen boyutta rastgele sayılardan oluşan bir numpy array oluştur
    array = np.random.random(size)
    # Bellek optimizasyonunun yapıldığını logla
    logging.info(f"Bellek optimizasyonu: {size} boyutunda array oluşturuldu.")
    # Oluşturulan array'i döndür
    return array

# Ana programın başlangıç noktası
if __name__ == "__main__":
    # Logging'i ayarla
    setup_logging()
    try:
        # Bellek optimizasyonu örneği olarak büyük bir array oluştur
        optimize_memory_usage(1_000_000)
        # 60 saniye boyunca CPU'yu yüksek performansla çalıştır
        heat_cpu(60)
    except ValueError as e:
        # Eğer ValueError alınırsa, hatayı logla
        logging.error(e)
