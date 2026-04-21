from rubpy import Client, filters
import os
import threading
from flask import Flask

# --- بخش ربات روبیکا ---
bot = Client(name="simple_bot")

@bot.on_message_updates(filters.commands(["start"]))
async def start(message):
    await message.reply("ربات روشن شد! بگو سلام.")

@bot.on_message_updates(filters.text)
async def reply_to_salam(message):
    if message.text == "سلام":
        await message.reply("سلام! خوبی؟ من حاضرم.")

# --- بخش وب سرور برای Render ---
app = Flask(__name__)

@app.route('/')
def home():
    return "ربات روبیکا فعال است."

def run_bot():
    print("ربات در حال اجراست...")
    bot.run()  # این دستور حلقه بی‌نهایت دارد

if __name__ == "__main__":
    # اجرای ربات در یک ترد جداگانه
    threading.Thread(target=run_bot, daemon=True).start()
    
    # اجرای وب سرور روی پورت تعیین شده توسط Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
