import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()
AGENT_BOT_TOKEN = os.getenv("ENGINEER_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Read from our external Vector Database text file!
def read_cisco_manual():
    try:
        with open("Cisco_BGP_Troubleshooting_Manual.txt", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return "Manual not found."

MOCK_CISCO_MANUAL = read_cisco_manual()

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /status <case_id>")
        return
        
    case_id = context.args[0]
    await update.message.reply_text(f"🔍 Fetching logs for {case_id}...")
    
    # Mocking fetching from Google Sheet
    await update.message.reply_text(
        f"📊 *Status for {case_id}*\n"
        f"Status: OPEN\n"
        f"Assigned Engineer: Pending\n"
        f"Severity: High\n"
        f"Root Cause Predict: Tower Overload / Backhaul",
        parse_mode="Markdown"
    )

async def resolve_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /resolve <case_id>")
        return
        
    case_id = context.args[0]
    
    # Mocking resolving the issue in Google Sheet
    await update.message.reply_text(f"✅ Case {case_id} has been marked as RESOLVED in Google Sheets. Customer notified.")

async def handle_noc_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # We trigger the RAG bot if the engineer mentions 'fetch', 'manual', or tags the bot
    if "fetch" in text.lower() or "manual" in text.lower() or "bgp" in text.lower():
        await update.message.reply_text("🤖 *Agentic NOC:* Querying Enterprise Vector DB for Cisco manuals and BGP logs...", parse_mode="Markdown")
        
        # Call Groq AI with the RAG context injected!
        prompt = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {
                    "role": "system",
                    "content": f"You are an elite NOC (Network Operations Center) AI assistant. You have retrieved this PDF manual from the Vector DB:\\n\\n{MOCK_CISCO_MANUAL}\\n\\nThe engineer has asked a question. Read the manual and provide the exact terminal commands they need to copy/paste, formatted in a markdown code block."
                },
                {"role": "user", "content": text}
            ]
        }
        
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                json=prompt
            )
            
            # Safely extract the response
            resp_json = response.json()
            if "choices" in resp_json:
                ai_reply = resp_json["choices"][0]["message"]["content"]
                await update.message.reply_text(ai_reply, parse_mode="Markdown")
            else:
                await update.message.reply_text("Error parsing Groq response. Check API key limits.")
        except Exception as e:
            await update.message.reply_text(f"Error reaching NOC AI: {e}")

def main():
    print("Starting Engineer Agent Bot with NOC RAG...")
    app = Application.builder().token(AGENT_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("resolve", resolve_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_noc_chat))
    
    print("NOC Agent Bot is listening...")
    app.run_polling()

if __name__ == "__main__":
    main()
