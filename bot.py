import telebot, threading, time
from hcloud import Client
from database import *
from dotenv import load_dotenv

load_dotenv()
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

def auto_check_servers():
    while True:
        accounts = get_all_accounts()
        for acc in accounts:
            try:
                hclient = Client(token=acc[2])
                for server in hclient.servers.get_all():
                    # چک کردن حجم ترافیک (اگر مصرف به ۹۵٪ رسید خاموش شود)
                    traffic_used = server.outgoing_traffic
                    traffic_limit = server.included_traffic
                    if traffic_used and traffic_limit and (traffic_used / traffic_limit) > 0.95:
                        server.power_off()
                        # اینجا می‌توانید نوتیفیکیشن تلگرام هم ارسال کنید
            except: pass
        time.sleep(300) # هر ۵ دقیقه

threading.Thread(target=auto_check_servers, daemon=True).start()
bot.polling()
