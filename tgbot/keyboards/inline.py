from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


cancel_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton("\U0001F3E0", callback_data="home"))  # Emoji "house"

menu_control_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("\U00002B05", callback_data="back"),  # Emoji "arrow_left"
            InlineKeyboardButton("\U0001F3E0", callback_data="home")  # Emoji "house"
        ]
    ]
)

only_confirming_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("\U00002714", callback_data="yes"),  # Emoji "heavy_check_mark"
            InlineKeyboardButton("\U0000274C", callback_data="no")  # Emoji "x"
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
        [
            InlineKeyboardButton("\U00002B05", callback_data="back"),  # Emoji "arrow_left"
            InlineKeyboardButton("\U0001F3E0", callback_data="home")  # Emoji "house"
        ]
    ]
)

fill_form_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Anketani to'ldirish", callback_data="fill_form")],
        [
            InlineKeyboardButton("\U00002B05", callback_data="back"),  # Emoji "arrow_left"
            InlineKeyboardButton("\U0001F3E0", callback_data="home")  # Emoji "house"
        ]
    ]
)

nations_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("🇺🇿 O'zbek", callback_data="uz")],  # Emoji "flag_uz"
        [InlineKeyboardButton("🇷🇺 Rus", callback_data="ru")],  # Emoji "flag_ru"
        [InlineKeyboardButton(u"\U0001F3C1 Boshqa", callback_data="other")],  # Emoji "checkered_flag"
        [
            InlineKeyboardButton("\U00002B05", callback_data="back"),  # Emoji "arrow_left"
            InlineKeyboardButton("\U0001F3E0", callback_data="home")  # Emoji "house"
        ]
    ]
)

edu_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("O'rta", callback_data="secondary")],
        [InlineKeyboardButton("O'rta maxsus", callback_data="secondary_special")],
        [InlineKeyboardButton("Oliy | Bakalavr", callback_data="bachalor")],
        [InlineKeyboardButton("Oliy | Magistr", callback_data="master")],
        [
            InlineKeyboardButton("\U00002B05", callback_data="back"),  # Emoji "arrow_left"
            InlineKeyboardButton("\U0001F3E0", callback_data="home")  # Emoji "house"
        ]
    ]
)

marital_status_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Turmush qurgan", callback_data="married")],
        [InlineKeyboardButton("Turmush qurmagan", callback_data="not_married")],
        [
            InlineKeyboardButton("\U00002B05", callback_data="back"),  # Emoji "arrow_left"
            InlineKeyboardButton("\U0001F3E0", callback_data="home")  # Emoji "house"
        ]
    ]
)

confirming_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(u"\U00002714", callback_data="yes"),  # Emoji "heavy_check_mark"
            InlineKeyboardButton(u"\U0000274C", callback_data="no")  # Emoji "x"
        ],
        [
            InlineKeyboardButton("\U00002B05", callback_data="back"),  # Emoji "arrow_left"
            InlineKeyboardButton("\U0001F3E0", callback_data="home")  # Emoji "house"
        ]
    ]
)

license_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(u"\U00002705 B", callback_data="b")],  # Emoji "white_check_mark"
        [InlineKeyboardButton(u"\U00002705 BC", callback_data="bc")],
        [InlineKeyboardButton(u"\U00002705 Boshqa", callback_data="other")],
        [InlineKeyboardButton(u"\U0000274E Yo'q", callback_data="no")],  # Emoji "negative_squared_cross_mark"
        [
            InlineKeyboardButton("\U00002B05", callback_data="back"),  # Emoji "arrow_left"
            InlineKeyboardButton("\U0001F3E0", callback_data="home")  # Emoji "house"
        ]
    ]
)

level_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("• 0%", callback_data="0")],
        [InlineKeyboardButton("• 25%", callback_data="25")],
        [InlineKeyboardButton("• 50%", callback_data="50")],
        [InlineKeyboardButton("• 75%", callback_data="75")],
        [InlineKeyboardButton("• 100%", callback_data="100")],
        [
            InlineKeyboardButton("\U00002B05", callback_data="back"),  # Emoji "arrow_left"
            InlineKeyboardButton("\U0001F3E0", callback_data="home")  # Emoji "house"
        ]
    ]
)

origin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Telegram", callback_data="telegram")],
        [InlineKeyboardButton("Instagram", callback_data="instagram")],
        [InlineKeyboardButton("Facebook", callback_data="facebook")],
        [InlineKeyboardButton("Tanishimdan", callback_data="acquainted")],
        [
            InlineKeyboardButton("\U00002B05", callback_data="back"),  # Emoji "arrow_left"
            InlineKeyboardButton("\U0001F3E0", callback_data="home")  # Emoji "house"
        ]
    ]
)

sending_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(u"\U00002714 Yuborish", callback_data="send"),  # Emoji "heavy_check_mark"
            InlineKeyboardButton(u"\U0000274C Bekor qilish", callback_data="home")  # Emoji "x"
        ]
    ]
)

admin_functions = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("\U0001F4CB Anketalar", callback_data="form_list"),  # Emoji "clipboard"
            InlineKeyboardButton("\U0001F4C8 Statistika", callback_data="stats"),  # Emoji "chart_with_upwards_trend"
            InlineKeyboardButton("\U00002709 E'lon berish", callback_data="mailing"),  # Emoji "envelope"
        ],
        [
            InlineKeyboardButton(text="\U0001F3E0", callback_data="home")  # Emoji "house"
        ]
    ]
)

admin_functions_state_stats = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("\U0001F4CB Anketalar", callback_data="form_list"),  # Emoji "clipboard"
            InlineKeyboardButton("\U00002709 E'lon berish", callback_data="mailing"),  # Emoji "envelope"
        ],
        [InlineKeyboardButton(text="\U0001F3E0", callback_data="home")]  # Emoji "house"
    ]
)

admin_functions_state_mailing = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("\U0001F4CB Anketalar", callback_data="form_list"),  # Emoji "clipboard"
            InlineKeyboardButton("\U0001F4C8 Statistika", callback_data="stats"),  # Emoji "chart_with_upwards_trend"
        ],
        [InlineKeyboardButton(text="\U0001F3E0", callback_data="home")]  # Emoji "house"
    ]
)
