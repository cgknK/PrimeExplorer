def floyd_cycle_detection(f, x0, max_iter=1000):
    tortoise = f(x0)
    hare = f(f(x0))
    iter_count = 0
    
    while tortoise != hare and iter_count < max_iter:
        tortoise = f(tortoise)
        hare = f(f(hare))
        iter_count += 1
    
    if iter_count == max_iter:
        return None  # Döngü bulunamadı veya sonsuz döngü var
    return tortoise, iter_count

# Örnek fonksiyon
def f(x):
    return (x * x + 1) % 255  # Rastgele bir fonksiyon

# Başlangıç değeri
x0 = 2
print(floyd_cycle_detection(f, x0))
