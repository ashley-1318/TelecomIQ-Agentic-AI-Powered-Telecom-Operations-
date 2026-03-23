# 🌐 TelecomIQ: AI-Powered Autonomous Telecom Operations & Churn Prevention

TelecomIQ is a next-generation, agentic AI architecture designed specifically for the telecom industry. It bridges the gap between reactive customer support (L1 Call Centers) and proactive Network Operations Center (NOC) engineering. By utilizing advanced LLMs, Multimodal Vision, autonomous Tool Use, and robust workflow automation, the system drastically reduces operational costs, mitigates churn, and accelerates network repair times.

---

## 🏗️ 1. Core System Architecture

The architecture acts as a unified central nervous system, merging customer complaints and backend server alerts into a single logic pipeline.

### **The Technology Stack**
* **Orchestrator:** **n8n** (Self-hosted) handles all routing, logic switches, conditional branching, and API integrations.
* **LLM Engine:** **Groq / Llama 3** handles millisecond-latency intelligence.
    * *Llama-4-Scout-17b:* Multimodal Vision capabilities.
    * *Llama-3.3-70b-versatile:* Complex reasoning and JSON formatting.
    * *Whisper-large-v3:* Voice-to-Text transcription.
* **Customer Interface:** **Telegram API** (allows text, photos, and voice memos).
* **Database / Dashboarding:** **Google Sheets** (Logging incidents, feeding live data to Looker Studio for executive overview).

---

## 💡 2. The Four Pillar Innovations

1. **Zero-Touch Pre-emptive Customer Care:** Automates customer apologies and issues data compensations *before* the customer realizes the network is down by polling Edge Servers (simulated by Distill.io) and querying CRM databases.
2. **Multimodal Router Diagnostics:** Customers can send photos of their hardware. The AI analyzes the router's physical LEDs (e.g., Red LOS light) to diagnose fiber cuts without human intervention.
3. **Sentiment-Driven Churn Prevention:** The AI calculates an `Anger_Score (1-10)` from customer text. If the score is extreme and the issue is billing-related, the AI automatically authorizes a Rs. 500 courtesy credit to save the contract.
4. **Agentic RAG for NOC Engineers:** A specialized autonomous bot (`agent_bot.py`) acts alongside human engineers in the NOC Group Chat. It intercepts commands, queries a Vector DB of mock Cisco/Ericsson router manuals, and provides precise terminal commands to reset hardware.

---

## 🔀 3. N8N Node Workflow & Logic Routing

The core `telecomiq_unified_workflow.json` pipeline is triggered by a single Master Webhook and split using a **Logic Switch Node**.

### **Trigger & Routing**
* **Master Webhook Trigger:** The single entry-point for all incoming data (Telegram payloads & Backend Server polling).
* **Logic Router (Switch):** Examines the JSON payload. If it detects `event: major_outage_detected`, it routes to the **Proactive Path**. If it detects a standard `message`, it routes to the **Reactive Path**.

### **Path A: Reactive Customer Triage (Top Row)**
1. **Code (Validate & Assign ID):** Generates a unique Case ID. If an `image_url` is present, it dynamically swaps the Groq API prompt to use the Llama-4 Vision model.
2. **HTTP Request (Groq Classify):** First AI pass. Extracts `type`, `severity`, `location`, `sentiment`, and calculates an `anger_score (1-10)`.
3. **Code (History Lookup):** Simulates checking historic tower logs. Instructs the AI to issue an automatic Rs. 500 credit if the `anger_score` is >8 for billing issues.
4. **HTTP Request (Groq Root Cause):** Second AI pass. Predicts the physical network root cause, recommends an engineering action, and drafts a highly polite, personalized customer reply.
5. **IF (Severity):** A conditional branch checking if the AI classified the issue as `High` severity.
    * **True:** Triggers **Telegram (Engineer Alert)**, blasting a markdown report to the Tier 3 NOC Group Chat.
6. **Telegram (Customer Reply):** Sends the conversational, AI-generated response back to the customer's personal device.
7. **Google Sheets (Log):** Appends all extracted AI intelligence (Case ID, Anger Score, Incident Type, Subtype) to the database for live Dashboard tracking.

### **Path B: Proactive Outage Automation (Bottom Row)**
1. **Query BSS/CRM Database:** Triggered by a simulated Distill.io NOC alert. Runs JavaScript to pull a list of all affected customer profiles (Mock CRM) living near the damaged tower.
2. **Item Lists (Loop):** Splits the array of affected customers and processes them one by one.
3. **Telegram (Pre-emptive Apology):** Sends an immediate, personalized "Zero-Touch" Telegram message directly to the customer offering a 1GB/2GB free data credit to offload L1 call support.
4. **Telegram (Engineer Mitigation Alert):** Alerts the NOC chat that automated mitigation was deployed successfully.

---

## 🐍 4. Python Microservices (The Agents)

The architecture is supported by three standalone Python agents operating concurrently:

1. **`bot.py` (The Customer Interface):** 
   * Constantly listens to the Customer Telegram bot.
   * Capable of downloading `.ogg` Voice Memos and passing them through the **Groq Whisper API** for instant Transcription.
   * Packages Image URLs and Text, forwarding them cleanly to the n8n Master Webhook.

2. **`agent_bot.py` (The NOC Agent):**
   * Sits silently in the Tier 3 Engineering Telegram Group.
   * When an engineer types `@TelecomIQ_Engineer_Bot fetch BGP logs...`, it intercepts the message.
   * Executes a simulated RAG (Retrieval-Augmented Generation) query against a mock Ericsson/Cisco PDF text block.
   * Uses Groq LLMs to analyze the manual and return the exact terminal SSH sequence the engineer must type to fix the tower.

3. **`distill_outage_simulator.py` (The Backend Poller):**
   * Acts as the simulated network edge monitor. 
   * When run, it fires a critical `major_outage_detected` JSON payload to n8n, tricking the Logic Switch into deploying the Proactive Outage Automation path.
