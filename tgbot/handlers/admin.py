import logging
import typing

from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from tgbot.keyboards.reply import admin_menu
from tgbot.misc.states import AdminStates
from tgbot.services.database import DBCommands


db = DBCommands("tgbot\db.db")


async def admin_start(message: types.Message):
    await message.reply("Xush kelibsiz, Admin!", reply_markup=admin_menu)
    await AdminStates.menu.set()


async def get_forms(message: types.Message, state: FSMContext):
    """  Send all forms' ids and names to admin  """
    forms_dict = await db.get_all_forms()
    text = ""
    inline_keyboard = types.InlineKeyboardMarkup()
    for key in forms_dict:
        text += f"{key}. {forms_dict[key]}\n"
        button = types.InlineKeyboardButton(text=key, callback_data=key)
        inline_keyboard.insert(button)
        logging.info(type(key))
    await message.answer(text, reply_markup=inline_keyboard)
    await AdminStates.forms.set()


async def send_form(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Yep!")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(get_forms, text_contains="\U0001F4CB Anketalar", state=AdminStates.menu,
                                is_admin=True)
    dp.register_callback_query_handler(send_form, regexp="^\d+$", state=AdminStates.forms)
