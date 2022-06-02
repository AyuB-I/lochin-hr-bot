import logging

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
    forms = await db.get_all_forms()
    text = ""
    for form in forms:
        text += f"{form}\n"
    await message.answer(text)
    await AdminStates.forms.set()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(get_forms, text_contains="\U0001F4CB Anketalar Ro'yhati", state=AdminStates.menu,
                                is_admin=True)
