from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.bot import dp, bot
from core.database import SessionLocal, User, Server, Plan
from core.hetzner_api import hetzner_manager
from config.settings import settings
import datetime

def get_main_menu(telegram_id: int):
    """ساخت منوی اصلی ربات با توجه به سطح دسترسی کاربر"""
    markup = InlineKeyboardMarkup(row_width=2)
    
    # دکمه‌های اصلی فروشگاه و مدیریت
    markup.add(
        InlineKeyboardButton("🛒 خرید سرور", callback_data="buy_server"),
        InlineKeyboardButton("⚙️ مدیریت سرویس‌ها", callback_data="manage_services")
    )
    
    # دکمه‌های مالی و کاربری
    markup.add(
        InlineKeyboardButton("💰 کیف پول", callback_data="wallet"),
        InlineKeyboardButton("🔗 زیرمجموعه‌گیری", callback_data="referral")
    )
    
    # دکمه شیشه‌ای استاندارد برای پنل وب (مخصوص ادمین) - بدون نیاز به مینی اپ
    if telegram_id == int(settings.ADMIN_ID):
        markup.add(
            InlineKeyboardButton("🌐 ورود به پنل مدیریت وب", url="https://your-domain.com/login")
        )
        
    return markup

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    """هندلر دستور استارت، ثبت‌نام کاربر و مدیریت لینک زیرمجموعه‌گیری"""
    db = SessionLocal()
    telegram_id = message.from_user.id
    
    # بررسی اینکه آیا کاربر از قبل در دیتابیس وجود دارد یا خیر
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    
    if not user:
        # دریافت آیدی معرف از لینک استارت (مثال: /start 123456789)
        invited_by = None
        args = message.get_args()
        if args and args.isdigit():
            invited_by = int(args)
            # اضافه کردن یک واحد به تعداد زیرمجموعه‌های شخص معرف
            inviter = db.query(User).filter(User.telegram_id == invited_by).first()
            if inviter:
                inviter.referral_count += 1
        
        # ثبت کاربر جدید در دیتابیس
        new_user = User(telegram_id=telegram_id, invited_by=invited_by)
        db.add(new_user)
        db.commit()
    
    db.close()
    
    text = (
        "به ربات مدیریت و فروش سرورهای ابری خوش آمدید! 🚀\n\n"
        "لطفاً از منوی زیر یکی از گزینه‌ها را انتخاب کنید:"
    )
    await message.answer(text, reply_markup=get_main_menu(telegram_id))

@dp.callback_query_handler(text="manage_services")
async def list_services(call: types.CallbackQuery):
    """نمایش لیست سرورهای خریداری شده توسط کاربر"""
    db = SessionLocal()
    servers = db.query(Server).filter(Server.user_id == call.from_user.id).all()
    db.close()
    
    if not servers:
        await call.answer("شما هیچ سرویس فعالی ندارید.", show_alert=True)
        return
        
    markup = InlineKeyboardMarkup(row_width=1)
    for s in servers:
        # ساخت دکمه برای هر سرور
        markup.add(InlineKeyboardButton(f"🖥 سرور (ID: {s.hetzner_id})", callback_data=f"server_menu_{s.id}"))
    
    markup.add(InlineKeyboardButton("بازگشت 🔙", callback_data="back_to_main"))
    
    await call.message.edit_text(
        "لیست سرورهای فعال شما:\nبرای مدیریت، روی سرور مورد نظر کلیک کنید:", 
        reply_markup=markup
    )

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('server_menu_'))
async def server_manage_menu(call: types.CallbackQuery):
    """منوی مدیریت یک سرور خاص (روشن، خاموش، ری‌استارت)"""
    db_server_id = int(call.data.split('_')[2])
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🟢 روشن", callback_data=f"action_poweron_{db_server_id}"),
        InlineKeyboardButton("🔴 خاموش", callback_data=f"action_poweroff_{db_server_id}")
    )
    markup.add(
        InlineKeyboardButton("🔄 ری‌استارت", callback_data=f"action_reboot_{db_server_id}"),
        InlineKeyboardButton("بازگشت 🔙", callback_data="manage_services")
    )
    
    text = (
        f"⚙️ **پنل مدیریت سرور**\n"
        f"کد سیستم: `{db_server_id}`\n\n"
        "یکی از عملیات‌های زیر را انتخاب کنید:\n"
        "⚠️ توجه: کاربر امکان حذف سرور را ندارد."
    )
    await call.message.edit_text(text, reply_markup=markup, parse_mode="Markdown")

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('action_'))
async def process_server_action(call: types.CallbackQuery):
    """ارسال دستور اکشن (روشن/خاموش/ری‌استارت) به API هتزنر"""
    data_parts = call.data.split('_')
    action = data_parts[1] # poweron, poweroff, reboot
    db_server_id = int(data_parts[2])
    
    db = SessionLocal()
    # بررسی مالکیت سرور (جلوگیری از دسترسی غیرمجاز)
    server = db.query(Server).filter(Server.id == db_server_id, Server.user_id == call.from_user.id).first()
    
    if not server:
        db.close()
        await call.answer("سرور یافت نشد یا شما دسترسی به این سرور ندارید.", show_alert=True)
        return
        
    hetzner_id = int(server.hetzner_id)
    db.close()
    
    action_map = {
        "poweron": "power_on",
        "poweroff": "power_off",
        "reboot": "reboot"
    }
    
    await call.answer("در حال ارسال درخواست به دیتاسنتر...", show_alert=False)
    
    # فراخوانی متد مدیریت هتزنر
    result = hetzner_manager.power_action(hetzner_id, action_map.get(action))
    
    if result:
        await call.message.answer(f"✅ دستور `{action}` با موفقیت به سرور ارسال شد.", parse_mode="Markdown")
    else:
        await call.message.answer(f"❌ خطا در انجام عملیات. لطفاً وضعیت سرور را بررسی کنید.")

@dp.callback_query_handler(text="buy_server")
async def show_plans(call: types.CallbackQuery):
    """نمایش لیست پلن‌های موجود برای خرید"""
    db = SessionLocal()
    plans = db.query(Plan).all()
    db.close()
    
    if not plans:
        await call.answer("در حال حاضر پلنی برای فروش موجود نیست.", show_alert=True)
        return
        
    markup = InlineKeyboardMarkup(row_width=1)
    for p in plans:
        markup.add(InlineKeyboardButton(f"📦 {p.name} | {p.price} تومان", callback_data=f"buyplan_{p.id}"))
        
    markup.add(InlineKeyboardButton("بازگشت 🔙", callback_data="back_to_main"))
    
    await call.message.edit_text("لطفاً یکی از پلن‌های زیر را انتخاب کنید:", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('buyplan_'))
async def process_buy_plan(call: types.CallbackQuery):
    """پردازش خرید پلن، کسر موجودی، ساخت سرور و تخصیص پاداش زیرمجموعه‌گیری"""
    plan_id = int(call.data.split('_')[1])
    db = SessionLocal()
    
    user = db.query(User).filter(User.telegram_id == call.from_user.id).first()
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    
    if not user or not plan:
        db.close()
        await call.answer("خطا در یافتن اطلاعات. لطفاً دوباره تلاش کنید.", show_alert=True)
        return

    # بررسی موجودی کیف پول
    if user.balance < plan.price:
        db.close()
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💰 شارژ کیف پول", callback_data="wallet"))
        markup.add(InlineKeyboardButton("بازگشت 🔙", callback_data="buy_server"))
        
        await call.message.edit_text(
            f"❌ **موجودی شما کافی نیست.**\n\n"
            f"موجودی فعلی: `{user.balance}` تومان\n"
            f"قیمت پلن: `{plan.price}` تومان\n\n"
            f"لطفاً ابتدا کیف پول خود را شارژ کنید.",
            reply_markup=markup,
            parse_mode="Markdown"
        )
        return
        
    # نمایش پیام انتظار به کاربر
    await call.message.edit_text("⏳ در حال ساخت سرور در دیتاسنتر هتزنر... لطفاً چند لحظه صبر کنید.")
    
    # ساخت نام یکتا برای سرور
    timestamp = int(datetime.datetime.now().timestamp())
    server_name = f"zarvpn-{user.telegram_id}-{timestamp}"
    
    # ارسال درخواست ساخت سرور به هتزنر
    hetzner_server = hetzner_manager.create_server(
        name=server_name, 
        server_type="cx11" # اگر در دیتابیس نوع سرور را ذخیره کردید، می‌توانید آن را اینجا قرار دهید
    )
    
    if not hetzner_server:
        db.close()
        await call.message.edit_text("❌ خطا در ارتباط با هتزنر و ساخت سرور. هیچ مبلغی از حساب شما کسر نشد.")
        return
        
    # کسر هزینه از کیف پول کاربر
    user.balance -= plan.price
    
    # محاسبه تاریخ انقضا (۳۰ روز)
    expire_date = datetime.datetime.now() + datetime.timedelta(days=30)
    
    # ثبت سرور در دیتابیس
    new_server = Server(
        user_id=user.telegram_id,
        hetzner_id=str(hetzner_server.id),
        expire_date=expire_date,
        status="active"
    )
    db.add(new_server)
    
    # محاسبه پاداش زیرمجموعه‌گیری (در صورت اولین خرید)
    user_servers_count = db.query(Server).filter(Server.user_id == user.telegram_id).count()
    if user_servers_count == 0 and user.invited_by:
        inviter = db.query(User).filter(User.telegram_id == user.invited_by).first()
        if inviter:
            reward = plan.price * 0.10  # ۱۰٪ پاداش
            inviter.balance += reward
            # تلاش برای ارسال نوتیفیکیشن به معرف
            try:
                await bot.send_message(
                    inviter.telegram_id,
                    f"🎁 تبریک! زیرمجموعه شما اولین خرید خود را انجام داد و مبلغ `{reward}` تومان به کیف پول شما اضافه شد.",
                    parse_mode="Markdown"
                )
            except Exception:
                pass
    
    db.commit()
    db.refresh(new_server)
    server_db_id = new_server.id
    db.close()
    
    # نمایش پیام موفقیت
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("⚙️ مدیریت این سرور", callback_data=f"server_menu_{server_db_id}"))
    markup.add(InlineKeyboardButton("بازگشت به منوی اصلی 🔙", callback_data="back_to_main"))
    
    await call.message.edit_text(
        f"✅ **خرید با موفقیت انجام شد!**\n\n"
        f"🖥 **نام سرور:** `{server_name}`\n"
        f"💰 **مبلغ کسر شده:** `{plan.price}` تومان\n"
        f"📅 **تاریخ انقضا:** `{expire_date.strftime('%Y-%m-%d %H:%M')}`\n\n"
        f"سرور شما ساخته شد و پروسه نصب سیستم‌عامل در حال انجام است.",
        parse_mode="Markdown",
        reply_markup=markup
    )

@dp.callback_query_handler(text="back_to_main")
async def back_to_main_menu(call: types.CallbackQuery):
    """دکمه بازگشت به منوی اصلی"""
    telegram_id = call.from_user.id
    await call.message.edit_text(
        "منوی اصلی:", 
        reply_markup=get_main_menu(telegram_id)
    )
