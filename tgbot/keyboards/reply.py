from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("\U0001f4dd Ro'yhatdan o'tish"),  # Emoji "memo"
            KeyboardButton("\U0001f3e2 Korxona haqida")  # Emoji "office_building"
        ],
        [
            KeyboardButton("\U000026A1"),  # Emoji "Zap"
            KeyboardButton("\U00002699")  # Emoji "Gear"
        ]
    ],
    resize_keyboard=True
)

user_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("\U0001f4dd Ro'yhatdan o'tish"),  # Emoji "memo"
            KeyboardButton("\U0001f3e2 Korxona haqida")  # Emoji "office_building"
        ],
        [KeyboardButton("\U00002699")]  # Emoji "Gear"
    ],
    resize_keyboard=True
)
