import threading
import time
import requests
import os

def keep_service_awake():
    url ="https://django-ecommerce-a9l2.onrender.com/ping/"

    while True:
        try:
            response = requests.get(url, timeout=10)
            print(f"Pinged: {response.status_code}")
        except Exception as e:
            print(f"Ping failed: {e}")

        time.sleep(240)  