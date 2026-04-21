from rubpy import Client, filters

# --- اتصال ربات ---
bot = Client(name="simple_bot")

# --- دستور /start ---
@bot.on_message_updates(filters.commands(["start"]))
async def start(message):
    await message.reply("ربات روشن شد! برای دریافت عکس پروفایل خود، کلمه 'عکس پروفایل' را بفرستید.")

# --- دریافت و ارسال عکس پروفایل ---
@bot.on_message_updates(filters.text)
async def handle_profile_photo(message):
    if message.text == "عکس پروفایل":
        try:
            # دریافت اطلاعات عکس‌های پروفایل کاربر
            user_photos = await bot.get_profile_photos(message.author_guid)

            if user_photos and len(user_photos) > 0:
                # انتخاب اولین عکس پروفایل (اصلی)
                first_photo = user_photos[0]

                # استخراج شناسه فایل عکس (بسته به ساختار کتابخانه ممکن است متفاوت باشد)
                # در برخی نسخه‌ها ممکن است از 'file_id' یا 'id' استفاده شود.
                file_id = first_photo.get('file_id') or first_photo.get('id')

                if file_id:
                    # ارسال عکس به کاربر
                    await message.reply_photo(file_id, caption="عکس پروفایل شما:")
                else:
                    await message.reply("نتونستم عکس پروفایلت رو پیدا کنم!")
            else:
                await message.reply("شما عکس پروفایل ندارید!")
        except Exception as e:
            # مدیریت خطاهای احتمالی
            await message.reply(f"در دریافت عکس پروفایل خطایی رخ داد: {e}")

# --- اجرای ربات ---
print("ربات در حال اجراست...")
bot.run()
