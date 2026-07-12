from aiogram import Bot, Dispatcher, executor
from config.settings import settings
import logging

logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)

# این ایمپورت‌ها باعث می‌شوند ربات تمام دکمه‌ها را شناسایی کند
from bot.handlers import user_handlers
from bot.handlers import wallet_handlers
from bot.handlers import referral_handlers

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
