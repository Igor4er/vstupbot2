from aiogram import Dispatcher
from vb2.bot.markup import start_markup
from vb2.bot.utils.user_operations import load_text


async def start(message):
    text = await load_text(message)
    await message.answer(text["GREETINGS"], reply_markup=start_markup.start_keyboard())


async def help_bot(message):
    text = await load_text(message)
    await message.answer(text["HELP"])


def register(dp: Dispatcher):
    dp.register_message_handler(
        commands=["start"], commands_prefix="!/", callback=start
    )
    dp.register_message_handler(
        commands=["help"], commands_prefix="!/", callback=help_bot
    )
