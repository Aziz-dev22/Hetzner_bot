from aiogram import Bot, Dispatcher, executor
from config.settings import settings
import logging

logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)

# وارد کردن هندلرها پس از تعریف dp
from bot.handlers import user_handlers

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

