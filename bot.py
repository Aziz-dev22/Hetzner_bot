import telebot, threading, time, os
from hcloud import Client
from database import *
from datetime import datetime, timedelta

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

# موتور خودکار: هر ۵ دقیقه چک می‌کند
def auto_scheduler():
    while True:
        # ۱. نوتیس ۲ روز قبل انقضا (هر ۶ ساعت)
        # ۲. حذف خودکار در صورت اتمام زمان
        # ۳. چک کردن حجم و خاموشی در صورت اتمام
        # (اینجا منطق API برای سرورهای کاربران اجرا می‌شود)
        time.sleep(300)

threading.Thread(target=auto_scheduler, daemon=True).start()

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    data = call.data
    
    # مدیریت سرور توسط کاربر (خاموش، روشن، ری‌استارت، ریبیلد، پسورد)
    if data.startswith("srv_"):
        action, srv_id = data.split("_")[1], data.split("_")[2]
        # اینجا دستورات hcloud برای اعمال تغییرات روی srv_id قرار می‌گیرد
        bot.answer_callback_query(call.id, f"عملیات {action} انجام شد.")
    
    # اجازه پاک کردن سرور داده نمی‌شود (مگر توسط ادمین)
    elif data.startswith("del_"):
        bot.answer_callback_query(call.id, "شما اجازه حذف سرور را ندارید!", show_alert=True)

bot.polling(none_stop=True)
