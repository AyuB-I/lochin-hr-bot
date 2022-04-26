from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


confirming_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(u"\U00002714", callback_data="yes"),
            InlineKeyboardButton(u"\U0000274C", callback_data="no")
        ]
    ]
)

professions_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Sotuv menejer bo'limi", callback_data="sales_manager")],
        [InlineKeyboardButton("Reklama bo'limi", callback_data="advertising")],
        [InlineKeyboardButton("Moliya bo'limi", callback_data="finance")],
        [InlineKeyboardButton("Kadrlar bo'limi", callback_data="hr")],
        [InlineKeyboardButton("Buxgalteriya bo'limi", callback_data="accounting")],
        [InlineKeyboardButton("Marketing bo'limi", callback_data="marketing")],
        [InlineKeyboardButton(u"\U00002B05 Orqaga", callback_data="back")]
    ]
)

fill_form_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Anketani to'ldirish", callback_data="fill_form")],
        [InlineKeyboardButton(u"\U00002B05 Orqaga", callback_data="back")]
    ]
)
