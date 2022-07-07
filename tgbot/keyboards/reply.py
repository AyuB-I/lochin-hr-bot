from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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
