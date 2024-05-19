import network
import time

# Inicjalizacja interfejsu Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Konfiguracja sieci Wi-Fi
ssid = 'flaczki'
password = 'haslo1234'

# Łączenie się z siecią Wi-Fi
wlan.connect(ssid, password)

# Sprawdzenie stanu połączenia
while not wlan.isconnected():
    print('Łączenie się z siecią...')
    time.sleep(1)

print('Połączono z siecią Wi-Fi')
print('Adres IP:', wlan.ifconfig()[0])


# Rozłączenie się z siecią Wi-Fi
wlan.active(False)
wlan.disconnect()
print('Rozłączono z siecią Wi-Fi')

