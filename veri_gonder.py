import serial
import requests
import time

# Arduino portu
ser = serial.Serial('/dev/cu.usbserial-10', 9600)

url = "http://127.0.0.1:5001/api/sel"

while True:
    try:
        veri = ser.readline().decode().strip()

        data = {
            'su': veri,
            'toprak': 0,
            'yagmur': 0
        }

        r = requests.post(url, data=data)

        print("Arduino verisi:", veri, "| Sunucu cevabı:", r.text)

    except Exception as e:
        print("Hata:", e)

    time.sleep(5)