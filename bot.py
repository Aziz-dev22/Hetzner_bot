import telebot, threading, time, os
from hcloud import Client
from database import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

def auto_check_logic():
    while True:
        # ۱. چک کردن ۵ دقیقه‌ای ترافیک و خاموشی خودکار
        # ۲. چک کردن نوتیس ۶ ساعته (۲ روز قبل انقضا)
        # ۳. چک کردن تاریخ انقضا و حذف سرور
        time.sleep(300)

threading.Thread(target=auto_check_logic, daemon=True).start()

@bot.callback_query_handler(func=lambda call: True)
def handle_queries(call):
    # دکمه‌های کنترلی کاربر (خاموش/روشن/ری‌استارت/تغییر پسورد)
    # اضافه کردن شرط if جهت مسدود کردن دکمه حذف برای کاربر
    if call.data.startswith("del_"):
        bot.answer_callback_query(call.id, "شما مجاز به حذف سرور نیستید!", show_alert=True)
    else:
        # اجرای دستورات مدیریتی سرور روی API هتزنر
        bot.answer_callback_query(call.id, "عملیات با موفقیت ارسال شد.")

bot.polling(none_stop=True)
