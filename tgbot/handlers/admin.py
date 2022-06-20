from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

from tgbot.keyboards.inline import admin_functions
from tgbot.keyboards.reply import admin_menu
from tgbot.misc.states import AdminStates
from tgbot.services.database import DBCommands

db = DBCommands("tgbot\db.db")


async def admin_start(message: types.Message, state: FSMContext):
    """  Greet the admin and send an admin menu  """
    await state.finish()
    await message.reply("Xush kelibsiz, Admin!", reply_markup=admin_menu)


async def show_admin_functions(message: types.Message):
    """  Handle the 'zap' button and direct the admin to the admin mode  """
    await message.answer("Admin Rejimi!", reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Mavjud funktsiyalar:", reply_markup=admin_functions)
    await AdminStates.admin_mode.set()


async def send_forms_list(call: types.CallbackQuery):
    """  Send a list of forms' ids and names to admin with inline keyboard of all forms' ids from db  """
    forms_dict = await db.get_all_forms()
    text = ""
    inline_keyboard = types.InlineKeyboardMarkup(row_width=10)
    for key in forms_dict:
        text += f"{key}. {forms_dict[key]}\n"
        button = types.InlineKeyboardButton(text=key, callback_data=key)
        inline_keyboard.insert(button)
    back_button = types.InlineKeyboardButton(text="\U00002B05", callback_data="back")
    home_button = types.InlineKeyboardButton(text="\U0001F3E0", callback_data="home")
    inline_keyboard.add(back_button, home_button)
    await call.message.edit_text(text, reply_markup=inline_keyboard)
    await AdminStates.forms.set()


async def send_form(call: types.CallbackQuery):
    """  Send a form which admin chose  """
    await call.answer(cache_time=30)
    form = await db.get_form(call.data)
    text = f"<b>Anketa ID:</b> {form['id']}\n" \
           f"<b>Ism va Familiya:</b> {form['full_name']}\n" \
           f"<b>Tug'ulgan sana:</b> {form['birthday']}\n" \
           f"<b>Telefon raqam:</b> {form['phone_number']}\n" \
           f"<b>Soha yo'nalishi:</b> {form['profession']}\n" \
           f"<b>Yashash manzil:</b> {form['address']}\n" \
           f"<b>Millat:</b> {form['nation']}\n" \
           f"<b>Ma'lumot:</b> {form['education']}\n" \
           f"<b>Oilaviy ahvol:</b> {form['marital_status']}\n" \
           f"<b>Xizmat safari:</b> {form['business_trip']}\n" \
           f"<b>Xarbiy xizmat:</b> {form['military']}\n" \
           f"<b>Sudlanganmi:</b> {form['criminal']}\n" \
           f"<b>Haydovchilik guvohnoma:</b> {form['driver_license']}\n" \
           f"<b>Shaxsiy avtomobil:</b> {form['personal_car']}\n" \
           f"<b>Rus tili:</b> {form['ru_lang']}\n" \
           f"<b>Ingiliz tili:</b> {form['eng_lang']}\n" \
           f"<b>Xitoy tili:</b> {form['chi_lang']}\n" \
           f"<b>Boshqa tillar:</b> {form['other_lang']}\n" \
           f"<b>Word dasturi:</b> {form['word_app']}\n" \
           f"<b>Excel dasturi:</b> {form['excel_app']}\n" \
           f"<b>1C dasturi:</b> {form['onec_app']}\n" \
           f"<b>Boshqa dasturlar:</b> {form['other_app']}\n" \
           f"<b>Biz haqimizda ma'lumot olgan manba:</b> {form['origin']}\n" \
           f"<b>Telegramdagi nomi:</b> {form['username']}\n" \
           f"<b>Jo'natilgan sana:</b> {form['date']}\n"
    message = await call.message.answer_photo(form["photo_id"])
    await call.bot.send_message(chat_id=call.from_user.id, text=text, reply_to_message_id=message.message_id, )


async def back(call: types.CallbackQuery, state: FSMContext):
    """  Handle the 'back' button and return to previous menu  """
    current_state = await state.get_state()
    if current_state == "AdminStates:forms" or current_state == "AdminStates:users":
        await call.message.edit_text("Mavjud funktsiyalar:", reply_markup=admin_functions)
        await AdminStates.admin_mode.set()


async def go_home(call: types.CallbackQuery, state: FSMContext):
    """  Handle the 'home' button and return to main menu  """
    await call.message.delete()
    await call.message.answer("Asosiy menyu!", reply_markup=admin_menu)
    await state.finish()


def register_admin(dp: Dispatcher):
    dp.register_callback_query_handler(go_home, text_contains="home", state=AdminStates)
    dp.register_callback_query_handler(back, text_contains="back", state=AdminStates)
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(show_admin_functions, text="\U000026A1", state="*", is_admin=True)
    dp.register_callback_query_handler(send_forms_list, text_contains="form_list", state=AdminStates.admin_mode)
    dp.register_callback_query_handler(send_form, regexp="^\d+$", state=AdminStates.forms)
