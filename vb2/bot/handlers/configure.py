from aiogram import Dispatcher, types
from vb2.bot.markup import config_markup, start_markup
from vb2.bot.utils.user_operations import load_text, add_user


async def configure(message):
    text = await load_text(message)
    markup = await config_markup.config_keyboard(message)
    if isinstance(message, types.Message):
        # Handle command logic
        await message.answer(text["CONFIGURATION"], reply_markup=markup)
    elif isinstance(message, types.CallbackQuery):
        # Handle query logic
        await message.message.edit_text(text["CONFIGURATION"], reply_markup=markup)


async def choose_language(query: types.CallbackQuery):
    text = await load_text(message=query)
    await query.message.edit_text(text["GREETINGS"], reply_markup=start_markup.start_keyboard())


async def set_language(query: types.CallbackQuery):
    await add_user(query)
    if query.data == "ua":
        await query.answer("Вибрано українську мову", show_alert=False)
    elif query.data == "en":
        await query.answer("Chosen English", show_alert=False)
    await configure(message=query)


def register(dp: Dispatcher):
    dp.register_message_handler(
        commands=["menu"], commands_prefix="!/", callback=configure
    )
    dp.register_callback_query_handler(configure, lambda query: query.data == "CONF")
    dp.register_callback_query_handler(choose_language, lambda query: query.data == "LANG")
    dp.register_callback_query_handler(
        set_language, lambda query: query.data in ["en", "ua"]
    )
