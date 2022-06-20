from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("\U0001f4dd Ro'yhatdan o'tish"),
            KeyboardButton("\U0001f3e2 Korxona haqida")
        ],
        [
            KeyboardButton("\U00002699")  # Unicode of the emoji "Gear"
        ]
    ],
    resize_keyboard=True
)

cancel_form_button = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("\U00002716 Bekor qilish"))

form_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("\U00002B05 Orqaga"),
            KeyboardButton("\U00002716 Bekor qilish")
        ]
    ],
    resize_keyboard=True
)

phonenum_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("\U0001f4de Raqamimni jo'natish", request_contact=True)
        ],
        [
            KeyboardButton("\U00002B05 Orqaga"),
            KeyboardButton("\U00002716 Bekor qilish")
        ]
    ],
    resize_keyboard=True
)

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("\U0001f4dd Ro'yhatdan o'tish"),
            KeyboardButton("\U0001f3e2 Korxona haqida")
        ],
        {
            KeyboardButton("\U000026A1"),  # Unicode of the emoji "Zap"
            KeyboardButton("\U00002699")  # Unicode of the emoji "Gear"
        }
    ],
    resize_keyboard=True
)