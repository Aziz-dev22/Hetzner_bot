from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.bot import dp, bot
from core.database import SessionLocal, User, Server, Plan
from core.hetzner_api import hetzner_manager
import datetime

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('buyplan_'))
async def process_buy_plan(call: types.CallbackQuery):
    """هندلر پردازش خرید پلن و کسر از کیف پول"""
    plan_id = int(call.data.split('_')[1])
    db = SessionLocal()
    
    # واکشی اطلاعات کاربر و پلن از دیتابیس
    user = db.query(User).filter(User.telegram_id == call.from_user.id).first()
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    
    if not user or not plan:
        db.close()
        await call.answer("خطا در یافتن اطلاعات. لطفاً دوباره تلاش کنید.", show_alert=True)
        return

    # ۱. بررسی موجودی کیف پول
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
        
    # اعلام وضعیت به کاربر (چون ساخت سرور در هتزنر ممکن است چند ثانیه زمان ببرد)
    await call.message.edit_text("⏳ در حال ساخت سرور در دیتاسنتر هتزنر... لطفاً چند لحظه صبر کنید.")
    
    # ۲. ساخت نام یکتا برای سرور در هتزنر
    timestamp = int(datetime.datetime.now().timestamp())
    server_name = f"zarvpn-{user.telegram_id}-{timestamp}"
    
    # ۳. ارسال درخواست به هتزنر برای ساخت سرور
    # نکته: در پروژه‌های بسیار بزرگ، بهتر است این بخش با asyncio.to_thread اجرا شود تا ربات بلاک نشود
    hetzner_server = hetzner_manager.create_server(
        name=server_name, 
        server_type="cx11" # برای حالت داینامیک می‌توانید این مقدار را از فیلدهای plan بگیرید
    )
    
    if not hetzner_server:
        db.close()
        await call.message.edit_text("❌ خطا در ارتباط با هتزنر و ساخت سرور. هیچ مبلغی از حساب شما کسر نشد.")
        return
        
    # ۴. کسر هزینه از کاربر
    user.balance -= plan.price
    
    # ۵. محاسبه تاریخ انقضا (۳۰ روز بعد)
    expire_date = datetime.datetime.now() + datetime.timedelta(days=30)
    
    # ۶. ثبت سرور در دیتابیس
    new_server = Server(
        user_id=user.telegram_id,
        hetzner_id=str(hetzner_server.id),
        expire_date=expire_date,
        status="active"
    )
    db.add(new_server)
    
    # ۷. سیستم پاداش زیرمجموعه‌گیری (اگر کاربر معرف دارد و اولین خریدش است)
    user_servers_count = db.query(Server).filter(Server.user_id == user.telegram_id).count()
    if user_servers_count == 0 and user.invited_by:
        inviter = db.query(User).filter(User.telegram_id == user.invited_by).first()
        if inviter:
            reward = plan.price * 0.10  # ۱۰٪ پاداش
            inviter.balance += reward
            # ارسال پیام به معرف (اختیاری - نیازمند مدیریت خطا در صورت بلاک بودن ربات توسط معرف)
            try:
                await bot.send_message(
                    inviter.telegram_id,
                    f"🎁 تبریک! زیرمجموعه شما اولین خرید خود را انجام داد و مبلغ `{reward}` تومان به کیف پول شما اضافه شد.",
                    parse_mode="Markdown"
                )
            except Exception:
                pass
    
    # ذخیره تغییرات دیتابیس
    db.commit()
    
    # دریافت آیدی دیتابیسِ سرورِ جدید برای ساخت دکمه مدیریت
    db.refresh(new_server)
    server_db_id = new_server.id
    db.close()
    
    # ۸. نمایش پیام موفقیت
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
