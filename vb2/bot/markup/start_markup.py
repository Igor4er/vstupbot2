from aiogram import types


def start_keyboard():
    language = types.InlineKeyboardMarkup(row_width=2)
    language.add(
        types.InlineKeyboardButton(text="🇺🇦", callback_data="ua"),
        types.InlineKeyboardButton(text="🇬🇧", callback_data="en"),
    )
    return language
