from aiogram import types
from bot.bot import dp, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.database import SessionLocal, User

@dp.callback_query_handler(text="referral")
async def referral_system(call: types.CallbackQuery):
    db = SessionLocal()
    user = db.query(User).filter(User.telegram_id == call.from_user.id).first()
    
    bot_info = await bot.get_me()
    referral_link = f"https://t.me/{bot_info.username}?start={call.from_user.id}"
    
    text = (
        "🔗 **لینک دعوت اختصاصی شما:**\n\n"
        f"`{referral_link}`\n\n"
        f"👥 تعداد زیرمجموعه‌های شما: {user.referral_count if user else 0} نفر\n"
        "🎁 با دعوت از هر کاربر و اولین خرید او، ۱۰٪ از مبلغ به کیف پول شما واریز می‌شود."
    )
    
    await call.message.edit_text(text, parse_mode="Markdown")
    db.close()
