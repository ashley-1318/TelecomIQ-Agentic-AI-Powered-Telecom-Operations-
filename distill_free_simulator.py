import time
import requests

URL = "http://localhost:8000/network.html"
WEBHOOK = "http://localhost:5678/webhook/telecomiq-webhook"

last_status = ""

while True:
    try:
        response = requests.get(URL)
        content = response.text

        if "OFFLINE" in content and last_status != "OFFLINE":
            print("🚨 Outage detected!")

            data = {
                "event": "major_outage_detected",
                "location": "Chennai-North",
                "customer_name": "Ashley Josco",
                "test_chat_id": "6628385427"
            }

            requests.post(WEBHOOK, json=data)

            last_status = "OFFLINE"

        elif "ONLINE" in content:
            last_status = "ONLINE"

    except Exception as e:
        print("Error:", e)

    time.sleep(5)