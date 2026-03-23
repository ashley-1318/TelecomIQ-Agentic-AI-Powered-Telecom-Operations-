import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Load configuration
load_dotenv()
# Using the local n8n webhook URL directly
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/telecomiq-webhook"
BOT_TOKEN = os.getenv("CUSTOMER_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    customer_name = update.message.chat.first_name
    customer_id = update.message.chat_id
    timestamp = update.message.date.isoformat()
    
    text = ""
    image_url = ""

    # Check if the user sent a photo
    if update.message.photo:
        photo_file = await update.message.photo[-1].get_file()
        image_url = photo_file.file_path
        text = update.message.caption if update.message.caption else "Customer sent an image of their router."
        await update.message.reply_text("Thanks! I am using Vision AI to analyze the lights on your router...")
        
    elif update.message.voice:
        # Handle Voice Memo
        await update.message.reply_text("Listened to your voice memo! Transcribing to text using Groq Whisper AI...")
        voice_file = await update.message.voice.get_file()
        file_path = "temp_voice.ogg"
        await voice_file.download_to_drive(file_path)
        
        # Call Groq Whisper
        with open(file_path, "rb") as f:
            response = requests.post(
                "https://api.groq.com/openai/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
                files={"file": ("temp_voice.ogg", f, "audio/ogg")},
                data={"model": "whisper-large-v3-turbo"}
            )
        
        text = response.json().get("text", "Could not transcribe audio.")
        # Optional: Print the transcription back to the user to show it worked
        await update.message.reply_text(f'🗣️ Transcribed: "{text}"\\nSending to TelecomIQ AI...')
        
    else:
        # It's a normal text message
        text = update.message.text
        await update.message.reply_text("Thanks for reaching out! TelecomIQ AI is analyzing your issue...")

    # Build payload
    payload = {
        "customer_name": customer_name,
        "customer_id": customer_id,
        "message": text,
        "image_url": image_url,
        "timestamp": timestamp
    }

    # Send securely to n8n
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload)
        print(f"Sent complaint to n8n. Status: {response.status_code}")
    except Exception as e:
        print(f"Error sending payload: {e}")

def main():
    print("Starting TelecomIQ Customer Bot with Vision Support...")
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Listen for Text, Photos, AND Voice Memos!
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.VOICE, handle_message))
    
    print("Customer bot is running and listening for text/photos...")
    app.run_polling()

if __name__ == '__main__':
    main()
