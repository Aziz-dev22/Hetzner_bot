import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from hcloud import Client
from dotenv import load_dotenv
from database import add_hetzner_account, get_all_accounts

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', 0))

bot = telebot.TeleBot(BOT_TOKEN)

def is_admin(user_id):
    return user_id == ADMIN_ID

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup(row_width=1)
    if is_admin(message.chat.id):
        markup.add(
            InlineKeyboardButton("🌐 ورود به پنل وب", url="http://YOUR_SERVER_IP:5000"),
            InlineKeyboardButton("➕ افزودن اکانت هتزنر", callback_data="add_account"),
            InlineKeyboardButton("🖥 لیست تمام سرورها (همه اکانت‌ها)", callback_data="list_servers")
        )
        bot.send_message(message.chat.id, "سلام مدیر. سیستم مدیریت چندگانه فعال است:", reply_markup=markup)
    else:
        markup.add(
            InlineKeyboardButton("💰 کیف پول", callback_data="wallet"),
            InlineKeyboardButton("🛒 خرید سرور جدید", callback_data="buy_server")
        )
        bot.send_message(message.chat.id, "به ربات خوش آمدید:", reply_markup=markup)

# ---------- بخش افزودن اکانت از داخل ربات ----------
@bot.callback_query_handler(func=lambda call: call.data == "add_account")
def ask_account_name(call):
    if not is_admin(call.message.chat.id): return
    msg = bot.send_message(call.message.chat.id, "لطفاً یک نام برای این اکانت هتزنر ارسال کنید (مثلاً: اکانت اول):")
    bot.register_next_step_handler(msg, process_account_name)

def process_account_name(message):
    account_name = message.text
    msg = bot.send_message(message.chat.id, f"نام '{account_name}' ثبت شد. حالا توکن API هتزنر را بفرستید:")
    bot.register_next_step_handler(msg, process_account_token, account_name)

def process_account_token(message, account_name):
    token = message.text
    if add_hetzner_account(account_name, token):
        bot.send_message(message.chat.id, "✅ اکانت با موفقیت به دیتابیس متصل شد.")
    else:
        bot.send_message(message.chat.id, "❌ این توکن قبلاً ثبت شده است.")

# ---------- بخش نمایش سرورها از تمام اکانت‌ها ----------
@bot.callback_query_handler(func=lambda call: call.data == "list_servers")
def list_servers(call):
    if not is_admin(call.message.chat.id): return
    
    accounts = get_all_accounts()
    if not accounts:
        bot.answer_callback_query(call.id, "هیچ اکانتی متصل نیست!", show_alert=True)
        return
    
    bot.send_message(call.message.chat.id, "⏳ در حال دریافت اطلاعات از تمامی اکانت‌ها...")
    
    for acc in accounts:
        acc_id, acc_name, acc_token = acc
        try:
            hclient = Client(token=acc_token)
            servers = hclient.servers.get_all()
            
            if not servers:
                bot.send_message(call.message.chat.id, f"📂 اکانت [{acc_name}]: سروری ندارد.")
                continue
                
            for server in servers:
                markup = InlineKeyboardMarkup(row_width=2)
                # ارسال توکن در دیتای دکمه برای مدیریت بعدی (نیازمند ذخیره وضعیت در دیتابیس در نسخه پیشرفته‌تر است)
                # در اینجا از آی‌دی سرور استفاده می‌کنیم
                markup.add(
                    InlineKeyboardButton("🟢 روشن", callback_data=f"start_{server.id}"),
                    InlineKeyboardButton("🔴 خاموش", callback_data=f"stop_{server.id}")
                )
                
                status = "🟢" if server.status == "running" else "🔴"
                text = f"🏢 اکانت: {acc_name}\n🖥 سرور: {server.name}\n🌐 آی‌پی: {server.public_net.ipv4.ip}\nوضعیت: {status}"
                bot.send_message(call.message.chat.id, text, reply_markup=markup)
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ خطا در اتصال به اکانت '{acc_name}'. توکن نامعتبر است.")
