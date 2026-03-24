import time
import requests
from datetime import datetime

BACKEND_URL = "http://backend:5000/items"

print("🚀 Notifier service started...")

def check_expiry():
    try:
        response = requests.get(BACKEND_URL)
        items = response.json()

        print("DEBUG: Items fetched ->", items)   # 👈 ADD THIS

        for item in items:
            expiry_date = datetime.strptime(item["expiry"], "%Y-%m-%d")
            days_left = (expiry_date - datetime.now()).days

            print(f"{item['name']} -> {days_left} days left")  # 👈 ADD

            if days_left <= 1 and days_left >= 0:
                print(f"⚠️ ALERT: {item['name']} expires in {days_left} day(s)!")

    except Exception as e:
        print("Error:", e)

while True:
    print("🔁 Running check...")
    check_expiry()
    time.sleep(10)