from aiogram import types
from vb2.bot.utils.json_operations import load_text


def config_keyboard(language="ua"):
    text = load_text(language)

    config = types.InlineKeyboardMarkup(row_width=2)
    config.add(types.InlineKeyboardButton(text=text["EXAM"], callback_data="EXAM"),
               types.InlineKeyboardButton(text=text["SPEC"], callback_data="SPEC"),
               types.InlineKeyboardButton(text=text["LANG"], callback_data="LANG"))
    return config
