from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from vb2.bot.utils.states import GetMark
from vb2.bot.markup import config_markup
from vb2.bot.utils.db_operations import load_text, add_user, update_results


async def configure(message):
    text = await load_text(message)
    markup = await config_markup.config_keyboard(message)
    if isinstance(message, types.Message):
        # Handle command logic
        await message.answer(text["CONFIGURATION"], reply_markup=markup)
    elif isinstance(message, types.CallbackQuery):
        # Handle query logic
        await message.message.answer(text["CONFIGURATION"], reply_markup=markup)


async def set_language(query: types.CallbackQuery):
    await add_user(query)
    if query.data == "ua":
        await query.answer("Вибрано українську мову", show_alert=True)
    elif query.data == "en":
        await query.answer("Chosen English", show_alert=True)


async def exam_config(query: types.CallbackQuery):
    text = await load_text(message=query)
    markup = await config_markup.exam_keyboard(query)
    await query.message.answer(text["EXAM"], reply_markup=markup)


async def choose_subject(query: types.CallbackQuery):
    text = await load_text(message=query)
    markup = await config_markup.subject_keyboard(query)
    await query.message.answer(text["EXAM"], reply_markup=markup)


async def get_mark(query:types.CallbackQuery, state: FSMContext):
    text = await load_text(message=query)
    subject = text[query.data]
    message = text[f"GET"].replace('{subject}', subject)
    await query.message.answer(message)
    await GetMark.mark.set()
    await state.update_data(subject=query.data)


async def save_mark(message: types.Message, state=FSMContext):
    text = await load_text(message)
    data = await state.get_data()
    await update_results(message, data)
    await message.answer(text["SAVED_MARK"])
    await state.finish()


def register(dp: Dispatcher):
    dp.register_message_handler(commands=["config"], commands_prefix="!/", callback=configure)
    dp.register_message_handler(state=GetMark.mark, callback=save_mark)
    dp.register_callback_query_handler(configure, lambda query: query.data == "CONF")
    dp.register_callback_query_handler(set_language, lambda query: query.data in ["en", "ua"])
    dp.register_callback_query_handler(exam_config, lambda query: query.data == "EXAM")
    dp.register_callback_query_handler(choose_subject, lambda query: query.data == "THIRD")
    dp.register_callback_query_handler(get_mark, lambda query: query.data in ["UA", "MATH", "HISTORY", "FOREIGN", "PHYSICS", "BIO", "CHEMISTRY"])
