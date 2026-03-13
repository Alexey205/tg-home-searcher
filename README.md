# HomeSearchBot 🏠🤖

[![Python](https://img.shields.io/badge/Python-3776AB?style=plastic&logo=python&logoColor=white)](https://python.org)
[![Telethon](https://img.shields.io/badge/Telethon-00AEEF?style=plastic&logo=telegram&logoColor=white)](https://docs.telethon.dev/)
[![Groq](https://img.shields.io/badge/Groq-f55036?style=plastic&logo=groq&logoColor=white)](https://groq.com/)
[![Llama 3](https://img.shields.io/badge/Llama_3.3-043b6e?style=plastic&logo=meta&logoColor=white)](https://ai.meta.com/llama/)
[![Asyncio](https://img.shields.io/badge/asyncio-1B2B34?style=plastic&logo=python&logoColor=white)](https://docs.python.org/3/library/asyncio.html)

An intelligent Telegram userbot and bot duo that automatically monitors real estate channels for apartment rentals, analyzes them using Groq's Llama 3 API, and forwards matching listings to you.

## Features ✨

- **Automatic Scraping:** Monitors specified Telegram channels via a user account.
- **AI Analysis:** Uses LLM (Llama 3.3 via Groq API) to extract structured data (rooms, price, features) from unstructured text.
- **Custom Filters:** Easily configure logic in the code to filter by room count and maximum price.
- **Instant Alerts:** Sends a beautifully formatted summary to you via a dedicated Telegram bot when a match is found.

---

## 🚀 Getting Started

### Prerequisites

You need the following API keys and accounts:
1. **Telegram API ID & Hash:** Used for the userbot to read channels.
2. **Telegram Bot Token:** Used to send you the final matched alerts.
3. **Groq API Key:** Used for the fast LLM text analysis.

### ⚙️ Step 1: Telegram Setup

#### 1.1 Getting API ID and API Hash (Userbot)
1. Go to [my.telegram.org](https://my.telegram.org) and log in with your phone number.
2. Go to **"API development tools"**.
3. Create a new application (fill in any app name and short name).
4. Save the **`App api_id`** and **`App api_hash`**.

#### 1.2 Creating a Telegram Bot
1. Open Telegram and search for **[@BotFather](https://t.me/botfather)**.
2. Send `/newbot` and follow the instructions to create a bot.
3. Save the **HTTP API Token** (this is your `BOT_TOKEN`).

#### 1.3 Getting Your User ID
1. Search for a bot like **[@userinfobot](https://t.me/userinfobot)** or **[@MissRose_bot](https://t.me/MissRose_bot)** in Telegram.
2. Send `/start` or `/info`.
3. Save your **Id** (this is your `MY_USER_ID`).

### 🧠 Step 2: Groq Setup
1. Go to the [Groq Console](https://console.groq.com/).
2. Create an account or log in.
3. Navigate to **API Keys** and click **"Create API Key"**.
4. Save the generated API key.

---

## 🛠️ Installation & Configuration

1. Clone or download this project.
2. Install the required dependencies:
   ```bash
   pip install telethon groq python-dotenv
   ```
3. Create a `.env` file in the root directory of the project and add your credentials:
   ```env
   TG_API_ID=your_api_id_here
   TG_API_HASH=your_api_hash_here
   BOT_TOKEN=your_bot_token_here
   MY_USER_ID=your_telegram_user_id_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. Edit `main_public.py` to customize your filters and channels:
   - Update `CHANNELS_TO_WATCH` with the Telegram usernames of the channels you want to monitor.
   - Adjust the filter logic in the `if` statement (e.g., target rooms and max price).

---

## ▶️ Running the Bot

Run the script using Python:
```bash
python main_public.py
```

**First Run Authentication:**
The first time you run the script, Telethon will ask you to log in to your user account to create `session_user.session`.
1. It will prompt you for your phone number (e.g., `+1234567890`).
2. Telegram will send a login code to your Telegram app. Enter it in the terminal.
3. If you have Two-Step Verification (2FA) enabled, enter your password when asked.

Once authenticated, the bot will start listening for new messages in the specified channels and analyzing them automatically!
