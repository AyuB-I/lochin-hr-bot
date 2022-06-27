from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


cancel_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton("\U0001F3E0", callback_data="home"))

menu_control_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("\U00002B05", callback_data="back"),  # The unicode of emoji "arrow_left"
            InlineKeyboardButton("\U0001F3E0", callback_data="home")  # The unicode of emoji "house"
        ]
    ]
)

phonenum_confirming_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(u"\U00002714", callback_data="yes"),  # The unicode of emoji "heavy_check_mark"
            InlineKeyboardButton(u"\U0000274C", callback_data="no")  # The unicode of emoji "x"
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
            InlineKeyboardButton("\U00002B05", callback_data="back"),  # The unicode of emoji "arrow_left"
            InlineKeyboardButton("\U0001F3E0", callback_data="home")  # The unicode of emoji "house"
        ]
    ]
)

fill_form_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Anketani to'ldirish", callback_data="fill_form")],
        [
            InlineKeyboardButton("\U00002B05", callback_data="back"),  # The unicode of emoji "arrow_left"
            InlineKeyboardButton("\U0001F3E0", callback_data="home")  # The unicode of emoji "house"
        ]
    ]
)

nations_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("🇺🇿 O'zbek", callback_data="uz")],
        [InlineKeyboardButton("🇷🇺 Rus", callback_data="ru")],
        [InlineKeyboardButton(u"\U0001F3C1 Boshqa", callback_data="other")],
        [
            InlineKeyboardButton("\U00002B05", callback_data="back"),  # The unicode of emoji "arrow_left"
            InlineKeyboardButton("\U0001F3E0", callback_data="home")  # The unicode of emoji "house"
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
            InlineKeyboardButton("\U00002B05", callback_data="back"),  # The unicode of emoji "arrow_left"
            InlineKeyboardButton("\U0001F3E0", callback_data="home")  # The unicode of emoji "house"
        ]
    ]
)

marital_status_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Turmush qurgan", callback_data="married")],
        [InlineKeyboardButton("Turmush qurmagan", callback_data="not_married")],
        [
            InlineKeyboardButton("\U00002B05", callback_data="back"),  # The unicode of emoji "arrow_left"
            InlineKeyboardButton("\U0001F3E0", callback_data="home")  # The unicode of emoji "house"
        ]
    ]
)

confirming_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(u"\U00002714", callback_data="yes"),  # The unicode of emoji "heavy_check_mark"
            InlineKeyboardButton(u"\U0000274C", callback_data="no")  # The unicode of emoji "x"
        ],
        [
            InlineKeyboardButton("\U00002B05", callback_data="back"),  # The unicode of emoji "arrow_left"
            InlineKeyboardButton("\U0001F3E0", callback_data="home")  # The unicode of emoji "house"
        ]
    ]
)

license_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(u"\U00002705 B", callback_data="b")],
        [InlineKeyboardButton(u"\U00002705 BC", callback_data="bc")],
        [InlineKeyboardButton(u"\U00002705 Boshqa", callback_data="other")],
        [InlineKeyboardButton(u"\U0000274E Yo'q", callback_data="no")],
        [
            InlineKeyboardButton("\U00002B05", callback_data="back"),  # The unicode of emoji "arrow_left"
            InlineKeyboardButton("\U0001F3E0", callback_data="home")  # The unicode of emoji "house"
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
            InlineKeyboardButton("\U00002B05", callback_data="back"),  # The unicode of emoji "arrow_left"
            InlineKeyboardButton("\U0001F3E0", callback_data="home")  # The unicode of emoji "house"
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
            InlineKeyboardButton("\U00002B05", callback_data="back"),  # The unicode of emoji "arrow_left"
            InlineKeyboardButton("\U0001F3E0", callback_data="home")  # The unicode of emoji "house"
        ]
    ]
)

sending_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(u"\U00002714 Yuborish", callback_data="send"),
            InlineKeyboardButton(u"\U0000274C Bekor qilish", callback_data="home")
        ]
    ]
)

admin_functions = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("\U0001F4CB Anketalar", callback_data="form_list"),
            InlineKeyboardButton("\U0001F464 Foydalanuvchilar", callback_data="user_list")
        ],
        [
            InlineKeyboardButton(text="\U0001F3E0", callback_data="home")  # The unicode of emoji "house"
        ]
    ]
)
