from aiogram import types
from vb2.bot.utils.user_operations import load_text


async def speciality_keyboard(message):
    """Propose user to choose searching method"""
    text = await load_text(message)
    cats_markup = types.InlineKeyboardMarkup(row_width=2)
    cats_markup.add(
        types.InlineKeyboardButton(text=text["CHOOSE_CODE"], callback_data="CODE"),
        types.InlineKeyboardButton(text=text["CHOOSE_SPEC"], callback_data="WORD"),
        types.InlineKeyboardButton(text=text["RETURN"], callback_data="CONF")
    )
    return cats_markup


async def spec_keyboard(found):
    """Get list of specialities from SupaBase"""
    spec_markup = types.InlineKeyboardMarkup(row_width=3)
    family = []
    for spec in found:
        family.append(
            types.InlineKeyboardButton(text=f"{spec.code} {spec.name}", callback_data=f"spec {spec.uuid}")
        )
    spec_markup.add(*family)
    return spec_markup


async def keyboard(message, uuid):
    """Propose user to choose searching method"""
    text = await load_text(message)
    buttons = types.InlineKeyboardMarkup(row_width=2)
    buttons.add(
        types.InlineKeyboardButton(text=text["CALCULATE"], callback_data=f"CALC {uuid}"),
        types.InlineKeyboardButton(text=text["FOLLOW"], callback_data="FLW"),
        types.InlineKeyboardButton(text=text["RETURN"], callback_data="SPEC")
    )
    return buttons
