from aiogram import Dispatcher, types
from vb2.bot.markup import spec_markup
from vb2.bot.utils.user_operations import load_text


async def cat_choosing(query: types.CallbackQuery):
    """Show a list of categories"""
    print(query.data)
    text = await load_text(message=query)
    markup = await spec_markup.category_keyboard()
    await query.message.answer(text["CHOOSE_CAT"], reply_markup=markup)


async def spec_choosing(query: types.CallbackQuery):
    """Show a list of specialities"""
    text = query.data.replace("cat ", "")
    await query.message.answer(text)


def register(dp: Dispatcher):
    dp.register_callback_query_handler(cat_choosing, lambda query: query.data == "SPEC")
    dp.register_callback_query_handler(spec_choosing, lambda query: "cat" in query.data)
