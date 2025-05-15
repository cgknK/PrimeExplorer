import wmi

# WMI nesnesi oluştur
w = wmi.WMI(namespace="root\\wmi")

# MSAcpi_ThermalZoneTemperature sınıfını kullanarak sıcaklık bilgisini al
try:
    temperature_info = w.MSAcpi_ThermalZoneTemperature()[0]
    # Sıcaklık değerini Kelvin cinsinden al ve Celsius'a çevir
    temperature = (temperature_info.CurrentTemperature / 10.0) - 273.15
    print(f"CPU Sıcaklığı: {temperature} °C")
except wmi.x_wmi as e:
    # Hata durumunda mesaj göster
    print("Sıcaklık bilgisi alınamadı. Hata:", e.com_error)
