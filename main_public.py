import os
import json
import asyncio
import logging
from telethon import TelegramClient, events
from groq import Groq
from dotenv import load_dotenv

# --- 1. SETTINGS ---
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()

# Check for required environment variables
required_vars = ['TG_API_ID', 'TG_API_HASH', 'BOT_TOKEN', 'MY_USER_ID', 'GROQ_API_KEY']
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    logger.error(f"❌ Missing variables in .env file: {', '.join(missing_vars)}")
    exit(1)

API_ID = int(os.getenv('TG_API_ID'))
API_HASH = os.getenv('TG_API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
MY_USER_ID = int(os.getenv('MY_USER_ID'))
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Groq Setup
client_groq = Groq(api_key=GROQ_API_KEY)
# Llama 3.3 - powerful model, ideal for complex instructions
AI_MODEL = "llama-3.3-70b-versatile" 

# --- CHANNELS LIST ---
# Add the usernames or links of the channels you want to monitor here
CHANNELS_TO_WATCH = [
    'example_real_estate_channel1', 
    'example_rentals_channel2'
]

# --- CLIENTS ---
client_user = TelegramClient('session_user', API_ID, API_HASH)
client_bot = TelegramClient('session_bot', API_ID, API_HASH)

# --- AI ANALYSIS FUNCTION (GROQ) ---
def analyze_with_ai(text):
    """AI creates a data structure for filtering AND a beautifully formatted description."""
    
    clean_text = text.replace('\n', ' ')[:1500] 

    # Base prompt instructing the AI
    prompt = f"""
    You are a real estate assistant. Your task is to:
    1. Extract technical data for filtering.
    2. Create a short, structured "Property Card" in English.

    Input text: "{clean_text}"
    Currency exchange rate: 1 USD = 42.8 UAH. (Adjust based on your local currency)

    Processing rules:
    - Rooms: look for "2 rooms", "3br", "1 bed" etc. If it's a studio, handle as 1.
    - Price: always convert so we have both USD and local currency if mentioned.

    Return ONLY a JSON object in the exact following format:
    {{
        "rooms": int (number of rooms),
        "price_usd": int,
        "price_local": int,
        "card_info": "Write the formatted card text here using line breaks (\\n). Use emojis. Include points: 📍 Location, 🏢 Floor, 📐 Area, 🔥 Heating, 🛠 Condition, 🐾 Pets allowed, 📝 Summary"
    }}
    """

    try:
        # Request to Groq API
        response = client_groq.chat.completions.create(
            messages=[
                # System message is important for Llama to strictly follow the JSON output format
                {"role": "system", "content": "You are a helpful assistant that replies exclusively in JSON format."},
                {"role": "user", "content": prompt}
            ],
            model=AI_MODEL,
            # This option guarantees valid JSON output structure
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        return json.loads(content)
        
    except Exception as e:
        logger.error(f"Groq error: {e}")
        return None

# --- MESSAGE HANDLER ---
@client_user.on(events.NewMessage(chats=CHANNELS_TO_WATCH))
async def handler(event):
    message_text = event.message.message
    
    if not message_text:
        return

    logger.info(f"📩 New message from {event.chat.username}. Analyzing...")

    data = analyze_with_ai(message_text)
    
    if not data:
        return

    rooms = data.get('rooms')
    price_usd = data.get('price_usd')
    
    # --- FILTERS ---
    # Example: Looking for 1 or 2 rooms
    is_suitable_rooms = rooms in [1, 2]
    
    # Example: Price <= $1000
    is_price_ok = (price_usd is not None and price_usd <= 1000)
    
    if is_suitable_rooms and is_price_ok:
        logger.info(f"✅ MATCH FOUND! {rooms} rooms for ${price_usd}.")
        
        alert_text = (
            f"🔥 **Found a {rooms}-room apartment!**\n\n"
            f"💵 **${data.get('price_usd')}** / {data.get('price_local')} local currency\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"{data.get('card_info')}\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"🔗 [Read original post](https://t.me/{event.chat.username}/{event.id})"
        )

        try:
            await client_bot.send_message(MY_USER_ID, alert_text, link_preview=True)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            
    else:
        logger.info(f"❌ Skipped: {rooms} rooms, ${price_usd}")

# --- STARTUP ---
async def main():
    logger.info("🚀 Starting bot (Groq API)...")
    await client_bot.start(bot_token=BOT_TOKEN)
    await client_user.start()
    logger.info("✅ Bot is actively listening to channels...")
    await client_user.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\nStopped.")
