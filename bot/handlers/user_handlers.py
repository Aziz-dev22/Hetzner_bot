from aiogram import types
from bot.bot import dp, bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.database import SessionLocal, Server

def get_main_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("خرید سرور", callback_data="buy_server"),
        InlineKeyboardButton("کیف پول", callback_data="wallet")
    )
    return markup

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("به پنل مدیریت سرور خوش آمدید:", reply_markup=get_main_menu())

@dp.callback_query_handler(text="manage_server")
async def manage_server(call: types.CallbackQuery):
    # دکمه‌های شیشه‌ای برای مدیریت سرور
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("روشن", callback_data="power_on"),
        InlineKeyboardButton("خاموش", callback_data="power_off")
    )
    markup.add(InlineKeyboardButton("ریستارت", callback_data="reboot"))
    await call.message.edit_text("پنل مدیریت سرور شما:", reply_markup=markup)

# هندلرهای مربوط به اجرای اکشن‌ها در HetznerManager در اینجا فراخوانی می‌شوند

