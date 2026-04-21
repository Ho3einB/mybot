import os
import threading
import asyncio
from flask import Flask
from rubpy import Client, filters

# -------------------------------
# ۱. بخش ربات روبیکا (همانند قبل)
# -------------------------------
# اتصال به حساب روبیکا با نام سشن دلخواه
bot = Client(name="simple_bot")

@bot.on_message_updates(filters.commands(["start"]))
async def start_handler(message):
    await message.reply(
        "👋 سلام! من ربات نمایش عکس پروفایل هستم.\n"
        "برای دیدن عکس پروفایلت، کافیه دستور زیر رو بفرستی:\n"
        "`عکس پروفایل`"
    )

@bot.on_message_updates(filters.text)
async def profile_photo_handler(message):
    # اگر کاربر دقیقا "عکس پروفایل" را تایپ کرد
    if message.text == "عکس پروفایل":
        # ارسال یک پیغام موقت برای نشان دادن در حال انجام بودن کار
        status_msg = await message.reply("🔍 در حال دریافت عکس پروفایل شما...")

        try:
            # --- دریافت اطلاعات عکس پروفایل از سرور روبیکا ---
            # از شناسه یکتای کاربر (author_guid) استفاده می‌کنیم.
            user_photos = await bot.get_profile_photos(message.author_guid)

            # بررسی اینکه آیا کاربر اصلا عکس پروفایل دارد یا خیر
            if user_photos and len(user_photos) > 0:
                # انتخاب اولین عکس (عکس اصلی پروفایل)
                first_photo = user_photos[0]

                # --- استخراج شناسه یکتای فایل (file_id) ---
                # ساختار دقیق بازگشتی از سرور ممکن است کمی متفاوت باشد.
                # معمولا در فیلدهای 'file_id' یا 'id' ذخیره می‌شود.
                file_id = first_photo.get('file_id') or first_photo.get('id')

                if file_id:
                    # --- ارسال عکس به کاربر ---
                    # عکس در نهایت با موفقیت ارسال می‌شود.
                    await message.reply_photo(file_id, caption="🖼️ عکس پروفایل شما:")
                    # حذف پیغام "در حال دریافت..." برای تمیزکاری
                    await status_msg.delete()
                else:
                    # اگر ساختار داده غیرمنتظره بود
                    await status_msg.edit("❌ نتونستم عکس پروفایلت رو پیدا کنم! (ساختار ناشناخته)")
            else:
                # اگر کاربر عکس پروفایل نداشته باشد
                await status_msg.edit("ℹ️ شما در حال حاضر عکس پروفایل ندارید!")

        except Exception as e:
            # مدیریت هرگونه خطای پیش‌بینی نشده
            await status_msg.edit(f"🚨 خطایی در دریافت عکس رخ داد: {e}")

# -------------------------------
# ۲. بخش وب سرور (برای حل مشکل Render)
# -------------------------------
# Render نیاز دارد که برنامه روی یک پورت مشخص به درخواست‌های HTTP پاسخ دهد.
# ما اینجا یک سرور کوچک با Flask راه‌اندازی می‌کنیم.

app = Flask(__name__)

@app.route('/')
def home():
    """پاسخی ساده برای زنده نگه داشتن سرویس"""
    return "✅ ربات روبیکا فعال است و عکس پروفایل ارسال می‌کند!"

def run_bot():
    """این تابع ربات را در یک event loop جداگانه اجرا می‌کند."""
    # ایجاد یک event loop جدید برای ربات
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    print("🤖 ربات در حال اتصال به روبیکا...")
    # اجرای ربات در این event loop
    bot.run()

if __name__ == "__main__":
    # اجرای ربات در یک Thread جداگانه تا برنامه اصلی مسدود نشود
    threading.Thread(target=run_bot, daemon=True).start()

    # اجرای وب سرور روی پورت تعیین شده توسط Render (پیش‌فرض ۱۰۰۰۰)
    port = int(os.environ.get("PORT", 10000))
    print(f"🌐 وب سرور روی پورت {port} در حال اجراست...")
    app.run(host="0.0.0.0", port=port)
