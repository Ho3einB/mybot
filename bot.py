from rubpy import Client, filters

# پورت رو با توجه به فیلترشکنت عوض کن (10808 معمولیه)
bot = Client(
    name="simple_bot",
    proxy="socks5://127.0.0.1:10808"  # این خط رو اضافه کن
)

@bot.on_message_updates(filters.commands(["start"]))
async def start(message):
    await message.reply("ربات روشن شد! بگو سلام.")

@bot.on_message_updates(filters.text)
async def reply_to_salam(message):
    if message.text == "سلام":
        await message.reply("سلام! خوبی؟ من حاضرم.")

print("ربات در حال اجراست...")
bot.run()
