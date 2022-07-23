from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("\U0001f4dd Ro'yhatdan o'tish"),  # Emoji "memo"
            KeyboardButton("\U0001f3e2 Korxona haqida")  # Emoji "office_building"
        ],
        [
            KeyboardButton("\U000026A1"),  # Emoji "Zap"
        ]
    ],
    resize_keyboard=True
)

user_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("\U0001f4dd Ro'yhatdan o'tish"),  # Emoji "memo"
            KeyboardButton("\U0001f3e2 Korxona haqida")  # Emoji "office_building"
        ]
    ],
    resize_keyboard=True
)
