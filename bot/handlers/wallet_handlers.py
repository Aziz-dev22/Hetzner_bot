from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.bot import dp, bot
from core.database import SessionLocal, User
from config.settings import settings

@dp.callback_query_handler(text="wallet")
async def show_wallet(call: types.CallbackQuery):
    """نمایش موجودی کیف پول و روش‌های شارژ"""
    db = SessionLocal()
    user = db.query(User).filter(User.telegram_id == call.from_user.id).first()
    balance = user.balance if user else 0
    db.close()
    
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("💳 شارژ ریالی (درگاه ایران)", callback_data="charge_irr"),
        InlineKeyboardButton("🪙 شارژ ارزی (کریپتو)", callback_data="charge_crypto"),
        InlineKeyboardButton("بازگشت 🔙", callback_data="back_to_main")
    )
    
    text = (
        f"💰 **کیف پول شما**\n\n"
        f"موجودی فعلی: `{balance}` تومان\n\n"
        "برای شارژ حساب، یکی از روش‌های زیر را انتخاب کنید:"
    )
    await call.message.edit_text(text, reply_markup=markup, parse_mode="Markdown")

@dp.callback_query_handler(text="charge_irr")
async def charge_irr_gateway(call: types.CallbackQuery):
    """هندلر درگاه پرداخت ریالی (زرین‌پال / نکست‌پی و ...)"""
    await call.answer("در حال ساخت لینک پرداخت...", show_alert=False)
    
    # در اینجا باید کدهای اتصال به API درگاه ایرانی قرار گیرد
    # به صورت تستی یک دکمه لینک‌دار فرضی می‌سازیم
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("پرداخت مبلغ 100,000 تومان", url="https://zarinpal.com/gateway/mock"),
        InlineKeyboardButton("بازگشت 🔙", callback_data="wallet")
    )
    
    await call.message.edit_text(
        "لینک پرداخت شما آماده است. لطفاً برای شارژ ریالی روی دکمه زیر کلیک کنید:", 
        reply_markup=markup
    )

@dp.callback_query_handler(text="charge_crypto")
async def charge_crypto_gateway(call: types.CallbackQuery):
    """نمایش گزینه‌های پرداخت ارزی با قابلیت انتخاب نوع ارز توسط ادمین"""
    markup = InlineKeyboardMarkup(row_width=2)
    
    # ادمین سیستم محدود به تتر نیست و می‌تواند هر ارزی را اینجا قرار دهد
    markup.add(
        InlineKeyboardButton("تتر (USDT-TRC20)", callback_data="crypto_USDT"),
        InlineKeyboardButton("ترون (TRX)", callback_data="crypto_TRX")
    )
    markup.add(InlineKeyboardButton("بازگشت 🔙", callback_data="wallet"))
    
    text = (
        "🪙 **شارژ ارزی (کریپتو)**\n\n"
        "سیستم پرداخت ما از ارزهای زیر پشتیبانی می‌کند. لطفاً ارز مورد نظر خود را انتخاب کنید:"
    )
    await call.message.edit_text(text, reply_markup=markup, parse_mode="Markdown")

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('crypto_'))
async def crypto_address_show(call: types.CallbackQuery):
    """نمایش آدرس ولت بر اساس ارز انتخاب شده"""
    coin = call.data.split('_')[1]
    
    # آدرس ولت‌های شما (در پروژه واقعی بهتر است این‌ها را در config.py ذخیره کنید)
    wallet_addresses = {
        "USDT": "T_YOUR_USDT_TRC20_WALLET_ADDRESS",
        "TRX": "T_YOUR_TRON_WALLET_ADDRESS"
    }
    
    selected_address = wallet_addresses.get(coin, "آدرس نامعتبر")
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅ واریز کردم (بررسی تراکنش)", callback_data="verify_payment"))
    markup.add(InlineKeyboardButton("بازگشت 🔙", callback_data="charge_crypto"))
    
    text = (
        f"ارز انتخاب شده: **{coin}**\n\n"
        f"لطفاً مبلغ مورد نظر خود را به آدرس زیر واریز کنید:\n\n"
        f"`{selected_address}`\n\n"
        "پس از واریز، حتماً روی دکمه «واریز کردم» کلیک کنید تا سیستم تراکنش را بررسی و کیف پول شما را شارژ کند."
    )
    await call.message.edit_text(text, reply_markup=markup, parse_mode="Markdown")

@dp.callback_query_handler(text="verify_payment")
async def verify_crypto_payment(call: types.CallbackQuery):
    """هندلر بررسی تراکنش پرداخت (نیاز به اتصال به API شبکه ترون/تتر)"""
    # منطق بررسی TXID و شارژ اتوماتیک دیتابیس در اینجا قرار می‌گیرد
    await call.answer("این بخش نیازمند دریافت TXID از شما و تایید شبکه است.", show_alert=True)
