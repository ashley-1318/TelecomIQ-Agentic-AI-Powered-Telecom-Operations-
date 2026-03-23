# TelecomIQ 📡
### Agentic AI-Powered Telecom Operations and Churn Prevention System

> A zero-cost, five-tool AI pipeline that transforms reactive telecom customer support into proactive, zero-touch, closed-loop automation — built in two weeks as a Generative AI internship capstone at Prodapt Solutions.

---

## 🚀 What It Does

TelecomIQ replaces the entire manual telecom complaint lifecycle with an AI-powered pipeline that:

- **Detects outages proactively** before customers even notice, using Distill.io to monitor telecom status pages
- **Triages complaints automatically** using Botpress as an L1 agent for FAQ handling and intent detection
- **Classifies and analyzes** every complaint using Groq LLM (type, severity, location, anger score)
- **Predicts root causes** from complaint context and historical incident data
- **Alerts engineers instantly** with structured AI-generated briefs to the NOC Telegram group
- **Replies to customers automatically** with personalized, empathetic messages and case IDs
- **Prevents churn** by detecting angry billing customers and authorizing Rs. 500 courtesy credits
- **Tracks SLA deadlines** with a background monitor that escalates breach-risk cases automatically
- **Handles voice and image input** — customers can send voice memos or router photos instead of typing

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
```

---

## 📂 Project Structure

```
TelecomIQ/
├── bot.py                          # Customer-facing Telegram bot (text, voice, image)
├── agent_bot.py                    # NOC engineer RAG bot (/status, /resolve, fetch commands)
├── distill_outage_simulator.py     # Mock Distill.io outage trigger for demo
├── telecomiq_unified_workflow.json # Master n8n workflow — import directly into n8n
├── sla_monitor_workflow.json       # Background SLA monitor workflow — import into n8n
├── .env.example                    # Environment variable template
├── requirements.txt                # Python dependencies
└── README.md
```

---

## ⚙️ Setup Guide

### Prerequisites

- n8n Cloud account (free tier) — [n8n.io](https://n8n.io)
- Groq API key (free) — [console.groq.com](https://console.groq.com)
- Distill.io account (free) — [distill.io](https://distill.io)
- Pabbly Connect account (free) — [pabbly.com/connect](https://www.pabbly.com/connect)
- Botpress account (free / self-hosted) — [botpress.com](https://botpress.com)
- Telegram account + two bots created via [@BotFather](https://t.me/botfather)
- Google account (for Sheets)
- Python 3.13+

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/your-username/TelecomIQ.git
cd TelecomIQ
```

---

### Step 2 — Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 3 — Configure Environment Variables

Copy `.env.example` to `.env` and fill in all values:

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
N8N_WEBHOOK_URL=https://your-n8n-instance.app.n8n.cloud/webhook/telecomiq-webhook

# Google Sheets
GOOGLE_SHEET_ID=your_google_sheet_id_here

# Pabbly
PABBLY_WEBHOOK_URL=https://connect.pabbly.com/workflow/sendwebhookdata/your_id_here
```

---

### Step 4 — Import n8n Workflows

1. Open your n8n Cloud dashboard
2. Go to **Workflows → Import from file**
3. Import `telecomiq_unified_workflow.json`
4. Import `sla_monitor_workflow.json`
5. Add your Groq API key, Telegram credentials, and Google Sheets OAuth inside each workflow's credential settings
6. Replace the three placeholder values in the workflow:
   - `YOUR_GROQ_API_KEY`
   - `YOUR_ENGINEER_GROUP_CHAT_ID`
   - `YOUR_GOOGLE_SHEET_ID`
7. Set both workflows to **Active**

---

### Step 5 — Set Up Botpress

1. Create a new bot in [Botpress Studio](https://studio.botpress.cloud)
2. Add a **Knowledge Base** with common telecom FAQ entries
3. Build the escalation flow:
   - Entry → NLU Classification → Condition (confidence > 0.75) → FAQ Reply OR Webhook escalation
4. In the Webhook action, paste your **Pabbly Connect webhook URL**
5. Connect the **Telegram channel** using your `TELEGRAM_CUSTOMER_BOT_TOKEN`

---

### Step 6 — Set Up Distill.io

1. Create a new monitor in [Distill.io](https://distill.io)
2. Enter the target telecom outage status page URL
3. Set monitor type to **Specific Element** and enter the CSS selector (e.g. `.outage-status`)
4. Set check interval to **5 minutes**
5. Under Notifications → enable **Webhook** and paste your **Pabbly Connect webhook URL**

---

### Step 7 — Set Up Pabbly Connect

1. Create a new Connection in [Pabbly Connect](https://connect.pabbly.com)
2. Set Trigger to **Webhook by Pabbly** — copy the generated URL
3. Give this URL to both Botpress (webhook action) and Distill.io (notification settings)
4. Add Action: **HTTP by Pabbly** → POST → your n8n webhook URL
5. Map fields: `customer_name`, `customer_id`, `message`, `source`, `timestamp`
6. For Distill payloads: add a Set Variable step to hard-code `event = major_outage_detected`

---

### Step 8 — Set Up Google Sheets

Create a new Google Sheet named **TelecomIQ Incidents** with a tab called **Incidents** and these exact column headers in Row 1:

```
CaseID | Customer | Location | Type | Severity | RootCause | AngerScore | Sentiment | Status | SLA_Deadline | Timestamp
```

---

### Step 9 — Run the Python Agents

Open three separate terminal windows and run:

```bash
# Terminal 1 — Customer-facing bot
python bot.py

# Terminal 2 — NOC engineer agent bot
python agent_bot.py

# Terminal 3 — Only needed for demo (simulates Distill.io outage trigger)
python distill_outage_simulator.py
```

---

## 🎬 Demo Walkthrough

### Demo 1 — Reactive Complaint (Text)

Send this message to your Telegram Customer Bot:

> *"My 4G has been dropping since morning, I can't work from home. This is really frustrating."*

**What happens:**
1. bot.py sends payload to Botpress
2. Botpress detects `network_issue` intent, confidence below threshold, escalates to Pabbly
3. Pabbly forwards to n8n
4. Groq classifies: `network_degradation | severity: high | anger_score: 7`
5. Historical lookup finds Tower A9 backhaul congestion pattern
6. Groq predicts root cause and drafts customer reply
7. Engineer NOC group receives structured alert
8. Customer receives personalized reply with Case ID and ETA
9. Google Sheets row appended

---

### Demo 2 — Proactive Outage (Before Any Complaint)

```bash
python distill_outage_simulator.py
```

**What happens:**
1. Outage payload fires to n8n
2. Switch node routes to Proactive Path
3. CRM lookup finds 3 affected customers near Tower A9
4. All 3 customers receive pre-emptive Telegram apology with 2GB free data credit
5. NOC group receives mitigation deployment confirmation

---

### Demo 3 — Voice Complaint

Send a voice memo to the Telegram Customer Bot saying anything about a network issue.

**What happens:**
1. bot.py downloads the `.ogg` file
2. Groq Whisper transcribes in ~300ms
3. Transcribed text enters the identical pipeline as a typed complaint

---

### Demo 4 — Image Diagnosis

Send a photo of a router with any LED light to the Customer Bot.

**What happens:**
1. bot.py extracts the image URL
2. n8n hot-swaps to `llama-4-scout-17b-16e-instruct`
3. Vision AI analyzes the LED state and diagnoses the hardware fault
4. High severity case auto-escalated to engineers

---

### Demo 5 — Churn Prevention

Send this angry billing message to the Customer Bot:

> *"I am absolutely furious. You have been overcharging me for months. I am cancelling today."*

**What happens:**
1. Groq scores `anger_score: 9` and detects `complaint_type: billing`
2. `authorize_credit: true` triggers Rs. 500 courtesy credit in the customer reply

---

### Demo 6 — NOC Engineer RAG

In the NOC Telegram group, type:

```
@TelecomIQ_NOC_Bot fetch BGP routing logs
```

**What happens:**
1. agent_bot.py intercepts the command
2. Groq queries mock Cisco/Ericsson manual context
3. Exact `clear ip bgp` terminal SSH sequence returned as a Markdown code block

---

## 📊 Results

| Metric | Result |
|---|---|
| Average pipeline execution time | 18–25 seconds |
| Voice transcription latency | 280–340ms |
| Classification accuracy | 9/10 complaint type, 10/10 severity |
| Proactive notification time | Under 10 seconds from outage signal |
| Sheets logging reliability | 100% — every case logged |
| Engineer alert delivery rate | 100% on high severity cases |
| Infrastructure cost | Rs. 0 — entirely free-tier tools |

---

## 🔮 Roadmap

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
| `N8N_WEBHOOK_URL` | The production webhook URL from your n8n workflow |
| `GOOGLE_SHEET_ID` | The ID string from your Google Sheet URL |
| `PABBLY_WEBHOOK_URL` | Your Pabbly Connect receiver webhook URL |

---

## 👤 Author

Built by **Ashley** — Generative AI Intern at Prodapt Solutions  
GitHub: [github.com/ashley-1318](https://github.com/ashley-1318)

---

## 📄 License

This project is for educational and demonstration purposes as part of a Generative AI internship capstone at Prodapt Solutions.
