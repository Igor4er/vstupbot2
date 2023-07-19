from aiogram import Dispatcher, types
from vb2.bot.markup import spec_markup
from vb2.bot.utils.user_operations import load_text
from vb2.bot.utils.exam import exam_calculation


async def calculus(query: types.CallbackQuery):
    """Show a list of categories"""
    message = query
    text = await load_text(message)
    result = await exam_calculation(query)
    message = text["RESULTS"] + " " + str(result)
    await query.message.answer(message)



def register(dp: Dispatcher):
    dp.register_callback_query_handler(calculus, lambda query: "CALC" in query.data)
