from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.bot import dp, bot
from core.database import SessionLocal, User

@dp.callback_query_handler(text="referral")
async def referral_system(call: types.CallbackQuery):
    """تولید لینک دعوت اختصاصی و نمایش آمار زیرمجموعه‌ها"""
    db = SessionLocal()
    user = db.query(User).filter(User.telegram_id == call.from_user.id).first()
    referral_count = user.referral_count if user else 0
    db.close()
    
    # دریافت یوزرنیم ربات به صورت داینامیک برای ساخت لینک دعوت
    bot_info = await bot.get_me()
    referral_link = f"https://t.me/{bot_info.username}?start={call.from_user.id}"
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("بازگشت 🔙", callback_data="back_to_main"))
    
    text = (
        "🔗 **بخش زیرمجموعه‌گیری و درآمدزایی**\n\n"
        "با دعوت از دوستان خود می‌توانید درآمد کسب کنید. فقط کافیست لینک زیر را برای آن‌ها ارسال کنید:\n\n"
        f"`{referral_link}`\n\n"
        f"👥 **تعداد زیرمجموعه‌های شما:** {referral_count} نفر\n\n"
        "🎁 **قوانین پورسانت:**\n"
        "با ثبت‌نام هر کاربر از طریق لینک شما و انجام **اولین خرید**، به صورت خودکار **5%** از مبلغ خرید او به کیف پول شما واریز می‌شود."
    )
    
    await call.message.edit_text(text, reply_markup=markup, parse_mode="Markdown")
