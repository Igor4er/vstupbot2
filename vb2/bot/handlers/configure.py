from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from vb2.bot.states import *
from vb2.bot.markup import config_markup
from vb2.bot.utils.json_operations import load_text, add_user


async def configure(message):
    text = await load_text(message)
    markup = config_markup.config_keyboard()
    await message.answer(text["CONFIGURATION"])
    await ExamsMarks.ua.set()


async def set_language(query: types.CallbackQuery):
    await add_user(query)
    if query.data == "ua":
        await query.answer("Вибрано українську мову", show_alert=True)
    elif query.data == "en":
        await query.answer("Chosen English", show_alert=True)


async def get_ua(message, state=FSMContext):
    ua = int(message.text)
    text = await load_text()
    if 100 <= ua <= 200:
        await state.update_data(ua=message.text)
        await message.answer(text["SUCCESS_UA"])


def register(dp: Dispatcher):
    dp.register_message_handler(commands=["poll"], commands_prefix="!/", callback=configure)
    dp.register_callback_query_handler(set_language, lambda query: query.data in ["en", "ua"])
