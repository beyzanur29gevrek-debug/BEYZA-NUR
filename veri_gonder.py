import requests
import random
import time

url = "http://127.0.0.1:5001/api/sel"  # Port 5001 ile eşleşmeli

while True:
    veri = {
        'su': random.randint(0, 200),
        'toprak': random.randint(0, 100),
        'yagmur': random.randint(0, 100)
    }
    try:
        r = requests.post(url, data=veri)
        print("Gönderilen veri:", veri, " | Sunucu yanıtı:", r.text)
    except Exception as e:
        print("Hata:", e)
    time.sleep(5)