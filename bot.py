import telebot, threading, time, os
from hcloud import Client
from database import *
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

def auto_check():
    while True:
        accounts = get_all_accounts()
        for acc in accounts:
            try:
                hclient = Client(token=acc[2])
                for server in hclient.servers.get_all():
                    # چک کردن حجم (اگر بیش از ۹۵٪ مصرف شده خاموش کن)
                    if server.included_traffic and server.outgoing_traffic:
                        if (server.outgoing_traffic / server.included_traffic) > 0.95:
                            server.power_off()
                            bot.send_message(os.getenv('ADMIN_ID'), f"⚠️ سرور {server.name} به دلیل اتمام حجم خاموش شد.")
            except: pass
        time.sleep(300) # هر ۵ دقیقه

threading.Thread(target=auto_check, daemon=True).start()

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "سلام! ربات مدیریت سرور آماده است.")

bot.polling(none_stop=True)
