import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from hcloud import Client
from hcloud.images.domain import Image
from dotenv import load_dotenv
from database import add_hetzner_account, get_all_accounts

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN', '').strip()
# تبدیل قطعی آیدی ادمین به رشته و حذف فاصله‌های اضافی
ADMIN_ID = str(os.getenv('ADMIN_ID', '')).strip()

bot = telebot.TeleBot(BOT_TOKEN)

def is_admin(user_id):
    # مقایسه ایمن آیدی‌ها به صورت رشته
    return str(user_id).strip() == ADMIN_ID

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        markup = InlineKeyboardMarkup(row_width=1)
        if is_admin(message.chat.id):
            # استفاده از دکمه شیشه‌ای برای لینک پنل وب 
            markup.add(
                InlineKeyboardButton("🌐 ورود به پنل مدیریت وب", url="http://YOUR_SERVER_IP:5000"),
                InlineKeyboardButton("➕ افزودن اکانت هتزنر", callback_data="add_account"),
                InlineKeyboardButton("🖥 مدیریت تمامی سرورها", callback_data="list_servers")
            )
            bot.reply_to(message, "سلام مدیر عزیز. پنل مدیریت یکپارچه شما آماده است:", reply_markup=markup)
        else:
            markup.add(
                InlineKeyboardButton("💰 کیف پول (تتر/ریالی)", callback_data="wallet"),
                InlineKeyboardButton("🛒 خرید سرور جدید", callback_data="buy_server"),
                InlineKeyboardButton("🔄 تغییر آی‌پی سرور من", callback_data="change_user_ip")
            )
            bot.reply_to(message, "به سیستم فروش و مدیریت ابری خوش آمدید:", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, f"خطای سیستمی: {e}")

# ---------- افزودن اکانت هتزنر ----------
@bot.callback_query_handler(func=lambda call: call.data == "add_account")
def ask_account_name(call):
    if not is_admin(call.message.chat.id): return
    msg = bot.send_message(call.message.chat.id, "نام اکانت هتزنر را وارد کنید (مثلا: اکانت اصلی):")
    bot.register_next_step_handler(msg, process_account_name)

def process_account_name(message):
    account_name = message.text
    msg = bot.send_message(message.chat.id, f"نام '{account_name}' تایید شد. توکن API را بفرستید:")
    bot.register_next_step_handler(msg, process_account_token, account_name)

def process_account_token(message, account_name):
    token = message.text
    if add_hetzner_account(account_name, token):
        bot.send_message(message.chat.id, "✅ اکانت با موفقیت ثبت و متصل شد.")
    else:
        bot.send_message(message.chat.id, "❌ این توکن قبلاً ثبت شده است.")

# ---------- مدیریت سرورها ----------
@bot.callback_query_handler(func=lambda call: call.data == "list_servers")
def list_servers(call):
    if not is_admin(call.message.chat.id): return
    
    accounts = get_all_accounts()
    if not accounts:
        bot.answer_callback_query(call.id, "هیچ اکانتی متصل نیست!", show_alert=True)
        return
    
    bot.send_message(call.message.chat.id, "⏳ در حال برقراری ارتباط با هتزنر...")
    
    for acc in accounts:
        acc_id, acc_name, acc_token = acc
        try:
            hclient = Client(token=acc_token)
            servers = hclient.servers.get_all()
            if not servers: continue
                
            for server in servers:
                markup = InlineKeyboardMarkup(row_width=2)
                # دکمه‌های مدیریتی برای هر سرور
                markup.add(
                    InlineKeyboardButton("🟢 روشن", callback_data=f"start_{server.id}"),
                    InlineKeyboardButton("🔴 خاموش", callback_data=f"stop_{server.id}"),
                    InlineKeyboardButton("🔄 ری‌استارت", callback_data=f"reboot_{server.id}"),
                    InlineKeyboardButton("🔑 ریست پسورد", callback_data=f"resetpass_{server.id}"),
                    InlineKeyboardButton("⚙️ ریبیلد", callback_data=f"rebuild_{server.id}"),
                    InlineKeyboardButton("🗑 حذف", callback_data=f"delete_{server.id}")
                )
                
                status = "🟢" if server.status == "running" else "🔴"
                text = f"🏢 اکانت: {acc_name}\n🖥 سرور: {server.name}\n🌐 آی‌پی: {server.public_net.ipv4.ip}\nوضعیت: {status}"
                bot.send_message(call.message.chat.id, text, reply_markup=markup)
        except Exception:
            bot.send_message(call.message.chat.id, f"❌ توکن اکانت '{acc_name}' نامعتبر است.")

# ---------- هندل کردن اکشن‌های سرور ----------
@bot.callback_query_handler(func=lambda call: call.data.split("_")[0] in ["start", "stop", "reboot", "resetpass", "rebuild", "delete"])
def handle_server_action(call):
    if not is_admin(call.message.chat.id): return
    
    action, server_id = call.data.split("_")[0], int(call.data.split("_")[1])
    accounts = get_all_accounts()
    target_server = None
    
    for acc in accounts:
        try:
            hclient = Client(token=acc[2])
            server = hclient.servers.get_by_id(server_id)
            if server:
                target_server = server
                break
        except:
            continue
            
    if not target_server:
        bot.answer_callback_query(call.id, "❌ سرور یافت نشد.", show_alert=True)
        return

    try:
        if action == "start":
            target_server.power_on()
            bot.answer_callback_query(call.id, "✅ روشن شد.")
        elif action == "stop":
            target_server.power_off()
            bot.answer_callback_query(call.id, "✅ خاموش شد.")
        elif action == "reboot":
            target_server.reboot()
            bot.answer_callback_query(call.id, "✅ ری‌استارت شد.")
        elif action == "resetpass":
            res = target_server.reset_password()
            bot.send_message(call.message.chat.id, f"🔑 پسورد جدید سرور {target_server.name}:\n`{res.root_password}`", parse_mode="Markdown")
            bot.answer_callback_query(call.id, "پسورد ریست شد.")
        elif action == "rebuild":
            # ریبیلد به اوبونتو 22.04 به صورت پیش‌فرض
            res = target_server.rebuild(image=Image(name="ubuntu-22.04"))
            bot.send_message(call.message.chat.id, f"⚙️ سرور در حال ریبیلد است.\nپسورد جدید:\n`{res.root_password}`", parse_mode="Markdown")
            bot.answer_callback_query(call.id, "ریبیلد آغاز شد.")
        elif action == "delete":
            target_server.delete()
            bot.send_message(call.message.chat.id, f"🗑 سرور {target_server.name} با موفقیت حذف شد.")
            bot.answer_callback_query(call.id, "حذف شد.")
    except Exception as e:
        bot.answer_callback_query(call.id, f"❌ خطا: {str(e)[:20]}")
