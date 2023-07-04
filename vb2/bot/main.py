from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from vb2.settings import settings
from handlers import start, configure

# Configure telegram bot
bot = Bot(token=settings.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


def __register_handlers(dp):
    start.register(dp)
    configure.register(dp)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=__register_handlers(dp))
