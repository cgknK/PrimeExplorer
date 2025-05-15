import concurrent.futures
import os
import time
import math
import logging

# Global end_time değişkeni
end_time = None

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def cpu_loader():
    # Belirli bir süre boyunca çalışacak
    global end_time
    while time.time() < end_time:
        [math.sqrt(x**3.14) for x in range(1000)] # Daha yoğun matematiksel işlem
    logging.info("Thread tamamlandı.")

def heat_cpu(duration):
    global end_time
    end_time = time.time() + duration
    num_workers = os.cpu_count()

    logging.info(f"CPU'yu {duration} saniye boyunca ısıtma başlatıldı.")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(cpu_loader) for _ in range(num_workers)]
        
        # Tüm thread'lerin bitmesini bekleyelim
        concurrent.futures.wait(futures)
    
    logging.info("Tüm thread'ler tamamlandı.")

if __name__ == "__main__":
    setup_logging()
    # 60 saniye boyunca CPU'yu ısıt
    heat_cpu(60)
