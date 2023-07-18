from aiogram import types
from vb2.common.db import categories


async def category_keyboard():
    """ Get list of categories from SupaBase and create keyboard for searching specialities by category"""
    cats = categories.all()
    cats_markup = types.InlineKeyboardMarkup(row_width=3)
    family = []
    for cat in cats:
        family.append(types.InlineKeyboardButton(text=cat.name, callback_data=f"cat {cat.uuid}"))
    cats_markup.add(*family)
    return cats_markup


async def spec_keyboard(uuid):
    pass
    """ Get list of specialities from SupaBase and create keyboard.
    Waiting for inserting data to DB 
    """

