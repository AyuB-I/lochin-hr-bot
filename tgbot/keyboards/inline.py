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
        [InlineKeyboardButton("Savdo menejment bo'limi", callback_data="sales_manager")],
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

nations_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("🇺🇿 O'zbek", callback_data="uz")],
        [InlineKeyboardButton("🇷🇺 Rus", callback_data="ru")],
        [InlineKeyboardButton(u"\U0001F3C1 Boshqa", callback_data="other")]
    ]
)

edu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("O'rta", callback_data="secondary")],
        [InlineKeyboardButton("O'rta maxsus", callback_data="secondary_special")],
        [InlineKeyboardButton("Oliy | Bakalavr", callback_data="bachalor")],
        [InlineKeyboardButton("Oliy | Magistr", callback_data="master")]
    ]
)

marital_status_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Turmush qurgan", callback_data="married")],
        [InlineKeyboardButton("Turmush qurmagan", callback_data="not_married")]
    ]
)

license_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(u"\U00002705 B", callback_data="b")],
        [InlineKeyboardButton(u"\U00002705 BC", callback_data="bc")],
        [InlineKeyboardButton(u"\U00002705 Boshqa", callback_data="other")],
        [InlineKeyboardButton(u"\U0000274E Yo'q", callback_data="no")],
    ]
)

level_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("• 0%", callback_data="0")],
        [InlineKeyboardButton("• 25%", callback_data="25")],
        [InlineKeyboardButton("• 50%", callback_data="50")],
        [InlineKeyboardButton("• 75%", callback_data="75")],
        [InlineKeyboardButton("• 100%", callback_data="100")],
    ]
)

origin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Telegram", callback_data="telegram")],
        [InlineKeyboardButton("Instagram", callback_data="instagram")],
        [InlineKeyboardButton("Facebook", callback_data="facebook")],
        [InlineKeyboardButton("Tanishimdan", callback_data="acquainted")]
    ]
)

sending_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(u"\U00002714 Yuborish", callback_data="send"),
            InlineKeyboardButton(u"\U0000274C Bekor qilish", callback_data="cancel")
        ]
    ]
)
