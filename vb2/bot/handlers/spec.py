from aiogram import Dispatcher, types
from vb2.bot.markup import spec_markup
from aiogram.dispatcher import FSMContext
from vb2.bot.utils.search_spec import search_by_code, search_by_word
from vb2.bot.utils.states import ChooseSpec
from vb2.bot.utils.user_operations import load_text


async def speciality(query: types.CallbackQuery):
    """Show a list of categories"""
    message = query
    text = await load_text(message)
    markup = await spec_markup.speciality_keyboard(message)
    await query.message.edit_text(text["CHOOSE_CAT"], reply_markup=markup)


async def looking_for_spec(query: types.CallbackQuery):
    text = await load_text(message=query)
    await query.message.edit_text(text[""])
    if query.data == "CODE":
        await ChooseSpec.search.set()
    elif query.data == "WORD":
        await ChooseSpec.words.set()


async def code_spec(message, state:FSMContext):
    text = await load_text(message)
    params = [lambda Specialities: message.text in Specialities.code]
    found = await search_by_code(params)

    markup = await spec_markup.spec_keyboard(found)
    await message.answer(text=text, reply_markup=markup)
    await state.finish()


async def word_spec(message, state:FSMContext):
    text = await load_text(message)
    specs = await search_by_word(message)
    markup = await spec_markup.spec_keyboard(specs)

    await message.answer(text=text["CHOSEN_SPEC"], reply_markup=markup)
    await state.finish()


async def spec_checking(query: types.CallbackQuery):
    """Show a list of specialities"""
    uuid = query.data.replace("spec ", "")
    await query.message.answer(uuid)


def register(dp: Dispatcher):
    dp.register_message_handler(state=ChooseSpec.search, callback=code_spec)
    dp.register_message_handler(state=ChooseSpec.words, callback=word_spec)
    dp.register_callback_query_handler(speciality, lambda query: query.data == "SPEC")
    dp.register_callback_query_handler(looking_for_spec, lambda query: query.data in ["CODE", "WORD"])
    dp.register_callback_query_handler(spec_checking, lambda query: "spec" in query.data)
