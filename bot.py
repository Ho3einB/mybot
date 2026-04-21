from rubpy import Client, filters
import os  # این خط رو اضافه کن

bot = Client(name="simple_bot")

@bot.on_message_updates(filters.commands(["start"]))
async def start(message):
    await message.reply("ربات روشن شد! بگو سلام.")

@bot.on_message_updates(filters.text)
async def reply_to_salam(message):
    if message.text == "سلام":
        await message.reply("سلام! خوبی؟ من حاضرم.")

# ---- این بخش جدید برای Render است ----
# Render نیاز دارد تا برنامه روی یک پورت شبکه گوش کند
if __name__ == "__main__":
    from flask import Flask
    import threading
    
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return "ربات در حال اجراست!"
    
    # اجرای ربات روبیکا در یک Thread جداگانه
    def run_bot():
        print("ربات در حال اجراست...")
        bot.run()
    
    threading.Thread(target=run_bot).start()
    
    # اجرای وب سرور Flask روی پورت ۱۰۰۰۰
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
# ---- پایان بخش جدید ----
