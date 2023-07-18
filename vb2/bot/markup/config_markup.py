from aiogram import types
from vb2.bot.utils.user_operations import load_text


async def config_keyboard(message):
    text = await load_text(message)

    config = types.InlineKeyboardMarkup(row_width=2)
    config.add(
        types.InlineKeyboardButton(text=text["EXAM_BUTTON"], callback_data="EXAM"),
        types.InlineKeyboardButton(text=text["SPEC_BUTTON"], callback_data="SPEC"),
        types.InlineKeyboardButton(text=text["LANG_BUTTON"], callback_data="LANG"),
    )
    return config
