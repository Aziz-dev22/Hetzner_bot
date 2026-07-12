from aiogram import types
from bot.bot import dp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.database import SessionLocal, User

@dp.callback_query_handler(text="wallet")
async def show_wallet(call: types.CallbackQuery):
    db = SessionLocal()
    user = db.query(User).filter(User.telegram_id == call.from_user.id).first()
    
    markup = InlineKeyboardMarkup(row_width=1)
    # دکمه‌های شارژ حساب
    markup.add(
        InlineKeyboardButton("💳 شارژ ریالی (درگاه ایران)", callback_data="charge_irr"),
        InlineKeyboardButton("🪙 شارژ کریپتو (Tether / TRX)", callback_data="charge_crypto")
    )
    
    text = f"💰 موجودی کیف پول شما: {user.balance if user else 0} تومان\n\n" \
           f"برای شارژ حساب یکی از روش‌های زیر را انتخاب کنید:"
           
    await call.message.edit_text(text, reply_markup=markup)
    db.close()

