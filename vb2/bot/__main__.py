from .config import dp, bot
from aiogram import executor

@dp.message_handler(commands=['start'])
async def start(message):
    await message.reply("Hello")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)