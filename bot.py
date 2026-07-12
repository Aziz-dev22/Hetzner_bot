import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from hcloud import Client
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', 0))
HETZNER_TOKEN = os.getenv('HETZNER_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)
hclient = Client(token=HETZNER_TOKEN)

def is_admin(user_id):
    return user_id == ADMIN_ID

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    if is_admin(message.chat.id):
        markup.add(InlineKeyboardButton("🌐 ورود به پنل مدیریت وب", url="http://YOUR_SERVER_IP:5000"))
        markup.add(InlineKeyboardButton("🖥 لیست تمام سرورها", callback_data="list_servers"))
        bot.send_message(message.chat.id, "سلام مدیر عزیز. به پنل مدیریت خوش آمدید:", reply_markup=markup)
    else:
        markup.add(InlineKeyboardButton("💰 کیف پول و شارژ", callback_data="wallet"))
        markup.add(InlineKeyboardButton("🛒 خرید سرور جدید", callback_data="buy_server"))
        bot.send_message(message.chat.id, "به ربات خرید و مدیریت سرور هتزنر خوش آمدید:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "list_servers")
def list_servers(call):
    if not is_admin(call.message.chat.id): return
    servers = hclient.servers.get_all()
    if not servers:
        bot.send_message(call.message.chat.id, "هیچ سروری یافت نشد.")
        return
    
    for server in servers:
        markup = InlineKeyboardMarkup(row_width=2)
        btn_start = InlineKeyboardButton("🟢 روشن", callback_data=f"action_start_{server.id}")
        btn_stop = InlineKeyboardButton("🔴 خاموش", callback_data=f"action_stop_{server.id}")
        btn_restart = InlineKeyboardButton("🔄 ری‌استارت", callback_data=f"action_restart_{server.id}")
        btn_change_ip = InlineKeyboardButton("🌐 چنج آی‌پی", callback_data=f"action_changeip_{server.id}")
        
        markup.add(btn_start, btn_stop, btn_restart, btn_change_ip)
        
        status = "روشن 🟢" if server.status == "running" else "خاموش 🔴"
        text = f"نام سرور: {server.name}\nآی‌پی: {server.public_net.ipv4.ip}\nوضعیت: {status}"
        bot.send_message(call.message.chat.id, text, reply_markup=markup)
