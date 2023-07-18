from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from vb2.bot.markup import exam_markup
from vb2.bot.utils.states import GetMark
from vb2.bot.utils.exam import update_results
from vb2.bot.utils.user_operations import load_text


async def exam_config(query: types.CallbackQuery):
    text = await load_text(message=query)
    markup = await exam_markup.exam_keyboard(query)
    await query.message.answer(text["EXAM"], reply_markup=markup)


async def choose_subject(query: types.CallbackQuery):
    text = await load_text(message=query)
    markup = await exam_markup.subject_keyboard(query)
    await query.message.answer(text["EXAM"], reply_markup=markup)


async def get_mark(query: types.CallbackQuery, state: FSMContext):
    text = await load_text(message=query)
    subject = text[query.data]
    message = text[f"GET"].replace("{subject}", subject)
    await query.message.answer(message)
    await GetMark.mark.set()
    await state.update_data(subject=query.data)


async def save_mark(message: types.Message, state=FSMContext):
    text = await load_text(message)
    data = await state.get_data()
    if 100 <= int(message.text) <= 200:
        await update_results(message, data)
        await message.answer(text["SAVED_MARK"])
        await state.finish()
    else:
        await GetMark.mark.set()


def register(dp: Dispatcher):
    dp.register_message_handler(state=GetMark.mark, callback=save_mark)
    dp.register_callback_query_handler(exam_config, lambda query: query.data == "EXAM")
    dp.register_callback_query_handler(
        choose_subject, lambda query: query.data == "THIRD"
    )
    dp.register_callback_query_handler(
        get_mark,
        lambda query: query.data
        in ["UA", "MATH", "HISTORY", "FOREIGN", "PHYSICS", "BIO", "CHEMISTRY"],
    )
