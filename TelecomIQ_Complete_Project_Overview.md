# 📡 TelecomIQ: Master Project Documentation
**AI-Powered Autonomous Telecom Operations & Churn Prevention System**

This document serves as the complete, end-to-end technical record of everything designed, coded, and built during the TelecomIQ Capstone project.

---

## 🏗️ 1. Project Overview & Business Impact
TelecomIQ was designed to prove that telecommunications companies can transition from reactive, manual customer support to **Proactive, Zero-Touch, Closed-Loop Automation**. 
The architecture drastically reduces L1 call-center volume, predicts financial churn, autonomously repairs edge hardware, and actively assists Tier 3 physical engineers in the field.

## 📂 2. Complete File Architecture
You successfully engineered 5 distinct codebases that interact flawlessly:
1. **`telecomiq_unified_workflow.json`**: The master n8n brain. An enormous multi-node pipeline handling Webhooks, AI logic, Hardware Auto-Fixes, and Database sorting.
2. **`sla_monitor_workflow.json`**: A secondary background n8n process running on a 30-minute schedule to constantly scan the DB for SLA breaches and blast escalation alarms.
3. **`bot.py`**: The Customer Telegram agent. Listens 24/7, handles Voice-to-Text via Groq Whisper API, and pipes raw data securely to n8n.
4. **`agent_bot.py`**: The NOC Engineering RAG bot. Intercepts engineer texts, queries a mock Vector Database (Cisco manuals), and uses Llama 3 to output exact executable terminal sequences.
5. **`distill_outage_simulator.py`**: The backend edge poller. Mocks an enterprise server-monitoring tool like Distill.io detecting an outage and forces the Proactive flow.

---

## 💡 3. The 6 Innovations Hand-Built

### 🟢 1. Zero-Touch Pre-emptive Care
* **Logic:** Instead of waiting for a customer to complain, `distill_outage_simulator.py` fires an outage payload to a Logic Router. 
* **Action:** The system queries the BSS/CRM for all customers physically located near "Tower A9" and sends them a Telegram text giving them 2GB of free data *before* their internet drops.

### 🔴 2. Sentiment-Driven "Churn Prevention"
* **Logic:** The AI processes angry text and calculates an `Anger_Score (1-10)`.
* **Action:** If the score exceeds 8 and the issue is "billing", the system is programmed to autonomously authorize a **Rs. 500 courtesy credit** inside its reply to save the customer's contract, logging the financial risk to a Google Sheets dashboard.

### 📷 3. Multimodal Router Diagnostics (Vision AI)
* **Logic:** Customers can upload images of their broken routers.
* **Action:** The system detects the `image_url` and dynamically hot-swaps the LLM model to `Llama-4-Scout-Vision`. The AI physically "looks" at the red LOS (Loss of Signal) light in the picture and accurately diagnoses fiber-cuts without human input.

### 🎙️ 4. Voice-to-Text L1 Call Center Offload
* **Logic:** To solve the problem of older generations refusing to type, users can send native Telegram Voice Memos.
* **Action:** `bot.py` downloads the `.ogg` file, fires it at Groq's Whisper AI, translates the speech into strict string text in 300ms, and runs it through the exact same workflow as if they had typed it.

### ⚙️ 5. Closed-Loop Network Auto-Fix
* **Logic:** The AI doesn't just inform users; it actually initiates repairs.
* **Action:** The n8n logic hits an `IF (Severity = High)` branch. It initiates a simulated REST API (`clear ip bgp soft`), then pings the router to verify 0% packet loss, closing the ticket and alerting the NOC group that the hardware was resolved via Zero-Touch.

### ⏳ 6. Auto-Priority Queue with SLA Clock
* **Logic:** Every complaint generates an `SLA_Deadline` variable (e.g., High = 2 hours, Low = 24 hours). 
* **Action:** `sla_monitor_workflow.json` scans Google Sheets constantly. If a ticket approaches expiration, it overrides the system and pings the Tier 4 NOC Duty Manager to prevent strict financial SLA-breach penalties.

---

## 🗄️ 4. The Google Sheets Database Structure
The AI flawlessly extracts unstructured chat data and heavily structure it into the following backend columns for Looker Studio visualization:
* `CaseID` *(e.g. CASE-28491)*
* `Customer` *(e.g. Josco)*
* `Location` *(e.g. Chennai-North)*
* `Type` *(e.g. Billing, Hardware, Degradation)*
* `Severity` *(Low, Medium, High, Critical)*
* `RootCause` *(AI's predicted underlying physical vector)*
* `Sentiment` *(Furious, Annoyed, Neutral)*
* `Anger_Score` *(1-10)*
* `Status` *(Closed-Loop Resolved, Open)*
* `SLA_Deadline` *(Auto-generated expiration timer)*
* `Timestamp`

---

## 🚀 5. Testing & Presentation Guide
To execute a flawless presentation of the entire project, run the following live tests:

1. **Activate Workflows:** Ensure `telecomiq_unified_workflow` is set to "Active" in n8n (or constantly hit Listen for test event). Run `python bot.py` and `python agent_bot.py`.
2. **Demo the Proactive Outage:** Run `python distill_outage_simulator.py` to trigger the 2GB network apology without chatting to a bot first.
3. **Demo Churn Prevention:** Send a furious text about overcharging directly to your Telegram Customer Bot and watch it issue a Rs. 500 credit instantly.
4. **Demo Multimodal Vision:** Send a picture of a router with a red light. Watch the AI classify it as high severity physical damage.
5. **Demo Voice Translation:** Send a voice memo into Telegram. Watch it transcribe to text and populate your Google Sheet beautifully.
6. **Demo Agentic RAG:** Ping your Engineer Bot in your NOC group chat (`fetch BGP logs`) and watch it read the Cisco Manual automatically and spit out a command sequence.
