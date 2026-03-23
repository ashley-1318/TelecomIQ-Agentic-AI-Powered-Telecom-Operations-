import requests
import os
from dotenv import load_dotenv

load_dotenv()

# The URL for the new master n8n webhook (which routes automatically via the Switch)
N8N_OUTAGE_WEBHOOK = "http://localhost:5678/webhook/telecomiq-webhook"

# We send your actual telegram chat ID so it texts your personal phone, 
# simulating you being a customer in the affected area!
# REPLACE WITH YOUR ACTUAL CUSTOMER CHAT ID IF NEEDED
test_chat_id = input("Enter your Telegram Chat ID: ")
test_name = input("Enter your Customer Name (e.g. Ashley): ")

payload = {
    "event": "major_outage_detected",
    "location": "Chennai-North, Sector 9",
    "severity": "CRITICAL - Backhaul Fiber Cut",
    "test_chat_id": test_chat_id,
    "customer_name": test_name
}

print("🚨 Distill.io detected a network outage! Sending webhook to n8n...")

try:
    response = requests.post(N8N_OUTAGE_WEBHOOK, json=payload)
    print(f"n8n Response: {response.status_code}")
    print("If n8n is 'Listening for test event', your workflow should now be executing perfectly!")
except Exception as e:
    print("Could not reach n8n webhook:", e)
