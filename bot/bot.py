from aiogram import Bot, Dispatcher, executor
from config.settings import settings

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)

# مثال برای تست ربات
@dp.message_handler(commands=['start'])
async def start(message):
    await message.reply("ربات با موفقیت فعال شد!")

def run_bot():
    executor.start_polling(dp, skip_updates=True)
