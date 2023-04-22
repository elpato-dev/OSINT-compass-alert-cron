import os
from dotenv import load_dotenv
from telegram import Bot, Message

# Load environment variables from .env file
load_dotenv()

# Get Telegram bot token from environment variable
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

async def send_telegram(message, chatid):
    # Create bot instance
    bot = Bot(token=bot_token)

    # Send message
    sent_message = await bot.send_message(chat_id=chatid, text=message)
    
    # Return the message object
    return sent_message
