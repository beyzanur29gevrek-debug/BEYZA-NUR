import serial
import requests
import time

ser = serial.Serial('COM4', 9600, timeout=1)

url = "https://sel-projesi.onrender.com/api/veri"

su = None
toprak = None
yagmur = None

while True:
    try:
        satir = ser.readline().decode('utf-8', errors='ignore').strip()

        if not satir:
            continue

        print("Arduino satırı:", satir)

        if satir.startswith("SU:"):
            su = float(satir.split(":")[1].strip())

        elif satir.startswith("TOPRAK:"):
            toprak = float(satir.split(":")[1].strip())

        elif satir.startswith("YAGMUR:"):
            yagmur = float(satir.split(":")[1].strip())

        if su is not None and toprak is not None and yagmur is not None:
            data = {
                "su": su,
                "toprak": toprak,
                "yagmur": yagmur
            }

            r = requests.post(url, json=data, timeout=10)

            print("Gönderilen veri:", data)
            print("Sunucu cevabı:", r.status_code, r.text)

            su = None
            toprak = None
            yagmur = None

    except Exception as e:
        print("Hata:", e)

    time.sleep(0.1)