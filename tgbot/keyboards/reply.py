from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from emoji import emojize as emo

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(u"\U0001f4dd Ro'yhatdan o'tish"),
            KeyboardButton(u"\U0001f3e2 Korxona haqida")
        ]
    ],
    resize_keyboard=True
)

cancel_form_button = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(u"\U00002716 Bekor qilish"))

form_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(u"\U00002B05 Orqaga"),
            KeyboardButton(u"\U00002716 Bekor qilish")
        ]
    ],
    resize_keyboard=True
)

phonenum_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(u"\U0001f4de Raqamimni jo'natish", request_contact=True)
        ],
        [
            KeyboardButton(u"\U00002B05 Orqaga"),
            KeyboardButton(u"\U00002716 Bekor qilish")
        ]
    ],
    resize_keyboard=True
)
