# TelecomIQ 📡
### Agentic AI-Powered Telecom Operations and Churn Prevention System

> A zero-cost, multi-tool AI pipeline that transforms reactive telecom customer support into proactive, zero-touch, closed-loop automation — built as a Generative AI internship capstone at Prodapt Solutions.

---

## 🚀 What It Does

TelecomIQ replaces the entire manual telecom complaint lifecycle with an AI-powered pipeline that:

- **Detects outages proactively** before customers even notice, using Distill.io to monitor telecom status pages
- **Triages complaints automatically** using Botpress as an L1 agent for FAQ handling and intent detection
- **Handles live voice calls** via a Vapi-powered AI voice assistant — customers can call in and speak naturally
- **Classifies and analyzes** every complaint using Groq LLM (type, severity, location, anger score)
- **Predicts root causes** from complaint context and historical incident data
- **Alerts engineers instantly** with structured AI-generated briefs to the NOC Telegram group
- **Replies to customers automatically** with personalized, empathetic messages and case IDs
- **Prevents churn** by detecting angry billing customers and authorizing Rs. 500 courtesy credits
- **Tracks SLA deadlines** with a background monitor that escalates breach-risk cases automatically
- **Handles voice memos and images** — customers can send .ogg audio or router photos via Telegram

**Average pipeline time: 18–25 seconds from complaint received to customer reply sent.**

---

## 🛠️ Tech Stack

| Tool | Role |
|---|---|
| **n8n Cloud** | Workflow orchestrator — all routing, AI logic, and integrations |
| **Distill.io** | Web change monitor — detects outage page changes, triggers proactive path |
| **Pabbly Connect** | Webhook bridge — normalizes payloads from Botpress and Distill.io |
| **Botpress** | L1 conversational agent — FAQ triage, intent detection, smart escalation |
| **Telegram Bot API** | Messaging interface — customer intake, engineer alerts, NOC group |
| **Vapi** | Voice AI platform — handles live inbound customer phone calls |
| **Groq API** | LLM engine — llama-3.3-70b, llama-4-scout (vision), whisper-large-v3 |
| **Google Sheets** | Incident database and Looker Studio dashboard data source |
| **Python 3.13** | Runtime for all three microservices |

---

## 🏗️ Architecture

```
                        ┌─────────────────────────────────┐
                        │        Master Webhook (n8n)      │
                        └───────────────┬─────────────────┘
                                        │
                          ┌─────────────▼──────────────┐
                          │      Switch Node (n8n)      │
                          └────────┬──────────┬─────────┘
                                   │          │
              ┌────────────────────▼─┐    ┌───▼────────────────────┐
              │   PATH A — REACTIVE  │    │  PATH B — PROACTIVE     │
              │                      │    │                          │
              │  Telegram Bot        │    │  Distill.io detects      │
              │       ↓              │    │  outage page change      │
              │  Botpress L1 Agent   │    │       ↓                  │
              │       ↓              │    │  Pabbly Connect          │
              │  Pabbly Connect      │    │       ↓                  │
              │       ↓              │    │  CRM Lookup (n8n)        │
              │  Groq — Classify     │    │       ↓                  │
              │       ↓              │    │  Loop customers          │
              │  History Lookup      │    │       ↓                  │
              │       ↓              │    │  Pre-emptive Telegram    │
              │  Groq — Root Cause   │    │  apology + 2GB credit    │
              │       ↓              │    │       ↓                  │
              │  IF Severity High?   │    │  NOC group alert         │
              │    ↓         ↓       │    └──────────────────────────┘
              │ Engineer   Customer  │
              │  Alert      Reply    │
              │       ↓              │
              │  Google Sheets Log   │
              └──────────────────────┘

              ┌──────────────────────────────────────────┐
              │     PATH C — VOICE AI (Vapi)             │
              │                                          │
              │  Customer makes a phone call             │
              │       ↓                                  │
              │  Vapi Tool Call Webhook (n8n)            │
              │       ↓                                  │
              │  Extract Vapi Payload                    │
              │       ↓                                  │
              │  TelecomIQ AI Agent (Groq + Memory)      │
              │       ↓                                  │
              │  Response Parser (structured JSON)       │
              │       ↓                                  │
              │  Format Vapi Response                    │
              │       ↓                                  │
              │  Respond to Vapi (spoken reply)          │
              │       ↓                                  │
              │  End-of-Call Webhook                     │
              │       ↓                                  │
              │  IF Escalate? → Alert Engineers          │
              │       ↓                                  │
              │  Log to Google Sheets                    │
              └──────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
TelecomIQ/
├── bot.py                              # Customer-facing Telegram bot (text, voice, image)
├── agent_bot.py                        # NOC engineer RAG bot (/status, /resolve, fetch)
├── distill_outage_simulator.py         # Mock Distill.io outage trigger for demo
├── telecomiq_unified_workflow.json     # Master n8n workflow — import into n8n
├── sla_monitor_workflow.json           # Background SLA monitor — import into n8n
├── TelecomIQ_Voice_Assistant.json      # Vapi voice call AI workflow — import into n8n
├── .env.example                        # Environment variable template
├── requirements.txt                    # Python dependencies
└── README.md
```

---

## 🎙️ Voice Assistant — TelecomIQ_Voice_Assistant.json

This n8n workflow adds a **live voice call channel** to TelecomIQ using [Vapi](https://vapi.ai). When a customer calls the Vapi phone number, this workflow handles the entire conversation in real time.

### Node Breakdown

| Node | What It Does |
|---|---|
| **Vapi Tool Call Webhook** | Receives tool call payloads from Vapi on every customer utterance |
| **Extract Vapi Payload** | Parses spoken text, tool call ID, and call session ID from the Vapi body |
| **TelecomIQ AI Agent** | Groq-powered LangChain agent — responds conversationally as a telecom support agent |
| **Conversation Memory** | Maintains a 10-message context window per call session using the call ID as key |
| **Response Parser** | Enforces structured JSON output with `response`, `category`, `escalate`, `resolved` |
| **Groq Model** | llama-3.3-70b-versatile — the LLM powering the AI agent |
| **Format Vapi Response** | Formats the AI reply into the exact JSON structure Vapi expects to speak aloud |
| **Respond to Vapi** | Returns the spoken response back to Vapi — the customer hears this in real time |
| **Vapi End-of-Call Webhook** | Triggers when the call ends — processes the full call report |
| **Process Call Report** | Extracts summary, duration, transcript, and escalation flag from the report |
| **Check Escalation** | IF node — routes to engineer alert if the call flagged a serious issue |
| **Alert Engineers (Telegram)** | Sends structured call summary to the NOC group if escalation was triggered |
| **Log to Google Sheets** | Appends the full call record to the Incidents sheet automatically |
| **Acknowledge End-of-Call** | Returns 200 OK to Vapi confirming the call report was received |

### AI Agent Behavior

The voice agent is configured to:
- Speak like a **polite, professional telecom support agent**
- Keep responses **short (1–2 sentences)** — optimized for voice, not text
- Ask **one question at a time** to guide the conversation step by step
- Internally classify issues as `network_issue`, `billing_issue`, `hardware_issue`, or `other`
- **Escalate automatically** on: no internet, confirmed outage, or repeated complaint pattern
- **Offer refund or credit** when customer is frustrated about billing
- Maintain **full conversation memory** across the entire call using the call ID

### Voice Assistant Setup

1. Create an account at [vapi.ai](https://vapi.ai)
2. Create a new assistant configured as a telecom support agent
3. Under **Tools** → add a custom tool with the server URL set to your `N8N_VAPI_WEBHOOK_URL`
4. Assign a phone number to the assistant
5. Import `TelecomIQ_Voice_Assistant.json` into n8n
6. Add Groq credentials to the **Groq Model** node
7. Add Telegram and Google Sheets credentials to the alert and log nodes
8. Set the workflow to **Active** and call your Vapi phone number

---

## ⚙️ Full Setup Guide

### Prerequisites

- n8n Cloud account (free tier) — [n8n.io](https://n8n.io)
- Groq API key (free) — [console.groq.com](https://console.groq.com)
- Distill.io account (free) — [distill.io](https://distill.io)
- Pabbly Connect account (free) — [pabbly.com/connect](https://www.pabbly.com/connect)
- Botpress account (free / self-hosted) — [botpress.com](https://botpress.com)
- Vapi account — [vapi.ai](https://vapi.ai)
- Telegram account + two bots via [@BotFather](https://t.me/botfather)
- Google account (for Sheets)
- Python 3.13+

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/ashley-1318/TelecomIQ.git
cd TelecomIQ
```

### Step 2 — Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Configure Environment Variables

```bash
cp .env.example .env
```

```env
# Telegram
TELEGRAM_CUSTOMER_BOT_TOKEN=your_customer_bot_token_here
TELEGRAM_ENGINEER_BOT_TOKEN=your_engineer_bot_token_here
TELEGRAM_ENGINEER_GROUP_ID=-100xxxxxxxxxx

# Groq
GROQ_API_KEY=your_groq_api_key_here

# n8n
N8N_WEBHOOK_URL=https://your-n8n.app.n8n.cloud/webhook/telecomiq-webhook
N8N_VAPI_WEBHOOK_URL=https://your-n8n.app.n8n.cloud/webhook/telecomiq-vapi

# Google Sheets
GOOGLE_SHEET_ID=your_google_sheet_id_here

# Pabbly
PABBLY_WEBHOOK_URL=https://connect.pabbly.com/workflow/sendwebhookdata/your_id_here
```

### Step 4 — Import All Three n8n Workflows

Go to **n8n → Workflows → Import from file** and import:

1. `telecomiq_unified_workflow.json` — main complaint pipeline
2. `sla_monitor_workflow.json` — background SLA breach monitor
3. `TelecomIQ_Voice_Assistant.json` — Vapi live voice call handler

Add credentials to each workflow and set all three to **Active**.

### Step 5 — Set Up Botpress

1. Create a new bot in [Botpress Studio](https://studio.botpress.cloud)
2. Add a Knowledge Base with common telecom FAQ entries
3. Build the escalation flow: Intent Classification → Condition (confidence > 0.75) → FAQ Reply OR Webhook escalation to Pabbly
4. Connect the Telegram channel using your `TELEGRAM_CUSTOMER_BOT_TOKEN`

### Step 6 — Set Up Distill.io

1. Create a monitor pointing to the telecom outage status page
2. Set type to **Specific Element** with CSS selector (e.g. `.outage-status`)
3. Set check interval to **5 minutes**
4. Enable Webhook notification → paste your Pabbly Connect URL

### Step 7 — Set Up Pabbly Connect

1. Trigger: **Webhook by Pabbly** — copy the URL and give it to Botpress and Distill.io
2. Action: **HTTP by Pabbly** → POST → your n8n webhook URL
3. Map fields: `customer_name`, `customer_id`, `message`, `source`, `timestamp`
4. For Distill payloads: add Set Variable → `event = major_outage_detected`

### Step 8 — Set Up Google Sheets

Create a sheet named **TelecomIQ Incidents** with tab **Incidents** and Row 1 headers:

```
CaseID | Customer | Location | Type | Severity | RootCause | AngerScore | Sentiment | Status | SLA_Deadline | Timestamp
```

### Step 9 — Run the Python Agents

```bash
# Terminal 1 — Customer Telegram bot
python bot.py

# Terminal 2 — NOC engineer agent bot
python agent_bot.py

# Terminal 3 — Demo only
python distill_outage_simulator.py
```

---

## 🎬 Demo Walkthrough

### Demo 1 — Live Voice Call (Vapi)
Call the Vapi phone number. Say: *"Hi, my internet has been down since this morning."*
The AI agent responds conversationally, classifies the issue, and escalates to the NOC group if serious. Full call is logged to Google Sheets at end of call.

### Demo 2 — Reactive Text Complaint (Telegram)
Send: *"My 4G has been dropping since morning, I can't work from home."*
Groq classifies → root cause predicted → engineer alerted → customer reply sent in ~22 seconds.

### Demo 3 — Proactive Outage
```bash
python distill_outage_simulator.py
```
3 customers near Tower A9 receive a pre-emptive apology with 2GB free data before they notice the outage.

### Demo 4 — Voice Memo (Telegram)
Send a voice memo to the Customer Bot. Groq Whisper transcribes in ~300ms and the text runs through the full pipeline.

### Demo 5 — Image Diagnosis (Telegram)
Send a photo of a router. Llama-4-Scout analyzes the LED state and diagnoses the hardware fault automatically.

### Demo 6 — Churn Prevention
Send: *"I am absolutely furious. You have been overcharging me for months. I am cancelling today."*
Anger score: 9/10 → Rs. 500 courtesy credit included in the automatic reply.

### Demo 7 — NOC Engineer RAG
In the NOC Telegram group type: `@TelecomIQ_NOC_Bot fetch BGP routing logs`
Exact `clear ip bgp` terminal SSH sequence returned as a Markdown code block in under 3 seconds.

---

## 📊 Results

| Metric | Result |
|---|---|
| Average pipeline execution time | 18–25 seconds |
| Voice call AI response latency | Under 2 seconds per turn |
| Telegram voice transcription latency | 280–340ms |
| Classification accuracy | 9/10 complaint type, 10/10 severity |
| Proactive notification time | Under 10 seconds from outage signal |
| Sheets logging reliability | 100% — every case logged |
| Engineer alert delivery rate | 100% on high severity cases |
| Infrastructure cost | Rs. 0 — entirely free-tier tools |

---

## 🔮 Roadmap

- [x] Telegram text, voice, and image complaint handling
- [x] Proactive outage detection via Distill.io
- [x] Botpress L1 FAQ triage and intent detection
- [x] Vapi live voice call AI assistant with conversation memory
- [ ] Replace simulated RAG with real FAISS vector index on Cisco PDF files
- [ ] Multilingual auto-response (Tamil, Hindi, Malayalam)
- [ ] Churn cohort scoring — weekly top 10 at-risk customer report
- [ ] WhatsApp Business API parallel channel
- [ ] Predictive tower failure detection from 30-day metrics
- [ ] Full production deployment with self-hosted n8n and PostgreSQL

---

## 📁 Environment Variables Reference

| Variable | Description |
|---|---|
| `TELEGRAM_CUSTOMER_BOT_TOKEN` | Token for the customer-facing Telegram bot |
| `TELEGRAM_ENGINEER_BOT_TOKEN` | Token for the NOC engineer Telegram bot |
| `TELEGRAM_ENGINEER_GROUP_ID` | Negative integer chat ID of the NOC Telegram group |
| `GROQ_API_KEY` | Your Groq API key from console.groq.com |
| `N8N_WEBHOOK_URL` | Webhook URL from the main n8n complaint workflow |
| `N8N_VAPI_WEBHOOK_URL` | Webhook URL from the Voice Assistant n8n workflow |
| `GOOGLE_SHEET_ID` | The ID string from your Google Sheet URL |
| `PABBLY_WEBHOOK_URL` | Your Pabbly Connect receiver webhook URL |

---

## 👤 Author

Built by **Ashley** — Generative AI Intern at Prodapt Solutions
GitHub: [github.com/ashley-1318](https://github.com/ashley-1318)

---

## 📄 License

This project is for educational and demonstration purposes as part of a Generative AI internship capstone at Prodapt Solutions.
