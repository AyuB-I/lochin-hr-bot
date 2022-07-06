import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

from tgbot.keyboards.inline import admin_functions, admin_function_form_list
from tgbot.keyboards.reply import admin_menu
from tgbot.misc.states import AdminStates
from tgbot.services.database import DBCommands

db = DBCommands("tgbot\db.db")


async def admin_start(message: types.Message, state: FSMContext):
    """  Greet the admin and send an admin menu  """
    await state.finish()
    await message.reply("Xush kelibsiz, Admin!", reply_markup=admin_menu)


async def show_admin_functions(message: types.Message, state: FSMContext):
    """  Handle the 'zap' button and direct the admin to the admin mode  """
    await message.answer("Admin Rejimi!", reply_markup=types.ReplyKeyboardRemove())
    functions_message = await message.answer("Mavjud funktsiyalar:", reply_markup=admin_functions)
    await state.update_data(functions_message_id=functions_message.message_id)
    await AdminStates.admin_mode.set()


async def send_form_list(call: types.CallbackQuery, state: FSMContext):
    """  Send a list of form ids and names of its owners to admin
    with inline keyboard of each form id from db  """
    await call.answer(cache_time=3)  # Simple anti-flood
    await state.finish()
    db_data = await db.get_forms()
    logging.info(db_data)
    forms_dict = db_data[0]
    first_row_id = db_data[1]  # ID of the first row in database
    smallest_id_dict = (list(forms_dict.keys()))[-1]  # The smallest ID in dictionary which are 16 rows of database
    biggest_id_dict = (list(forms_dict.keys()))[0]  # The biggest ID in dictionary which are 16 rows of database
    text = ""
    inline_keyboard = types.InlineKeyboardMarkup(row_width=5)
    for key in forms_dict:
        text += f"{key}. {forms_dict[key]}\n"
        button = types.InlineKeyboardButton(text=key, callback_data=key)
        inline_keyboard.insert(button)

    if not smallest_id_dict == first_row_id:
        next_button = types.InlineKeyboardButton(text="\U000023ED", callback_data="next")
        inline_keyboard.add(next_button)

    stats_button = types.InlineKeyboardButton(text="\U0001F4C8 Statistika", callback_data="stats")
    home_button = types.InlineKeyboardButton(text="\U0001F3E0", callback_data="home")
    inline_keyboard.add(stats_button, home_button)
    functions_message = await call.message.edit_text(text, reply_markup=inline_keyboard)
    await state.update_data(sent_forms=[], smallest_id_dict=smallest_id_dict, biggest_id_dict=biggest_id_dict,
                            functions_message_id=functions_message.message_id)
    await AdminStates.forms.set()


async def send_next_form_list(call: types.CallbackQuery, state: FSMContext):
    """  Send a list of form ids and names of its owners to admin
    with inline keyboard of each form id from db  """
    await call.answer(cache_time=1)  # Simple anti-flood
    async with state.proxy() as data:
        db_data = await db.get_forms(begin=data.get("smallest_id_dict"), key="next")
    logging.info(db_data)
    forms_dict = db_data[0]
    first_row_id = db_data[1]  # ID of the first row in database
    last_row_id = db_data[2]  # ID of the last row in database
    smallest_id_dict = (list(forms_dict.keys()))[-1]  # The smallest ID in dictionary which are 16 rows of database
    biggest_id_dict = (list(forms_dict.keys()))[0]  # The biggest ID in dictionary which are 16 rows of database
    text = ""
    inline_keyboard = types.InlineKeyboardMarkup(row_width=5)
    for key in forms_dict:
        text += f"{key}. {forms_dict[key]}\n"
        button = types.InlineKeyboardButton(text=key, callback_data=key)
        inline_keyboard.insert(button)

    if not biggest_id_dict == last_row_id:
        previous_button = types.InlineKeyboardButton(text="\U000023EE", callback_data="previous")
        inline_keyboard.add(previous_button)

    if not smallest_id_dict == first_row_id:
        next_button = types.InlineKeyboardButton(text="\U000023ED", callback_data="next")
        inline_keyboard.insert(next_button)

    stats_button = types.InlineKeyboardButton(text="\U0001F4C8 Statistika", callback_data="stats")
    home_button = types.InlineKeyboardButton(text="\U0001F3E0", callback_data="home")
    inline_keyboard.add(stats_button, home_button)
    functions_message = await call.message.edit_text(text, reply_markup=inline_keyboard)
    await state.update_data(sent_forms=[], smallest_id_dict=smallest_id_dict, biggest_id_dict=biggest_id_dict,
                            functions_message_id=functions_message.message_id)


async def send_previous_form_list(call: types.CallbackQuery, state: FSMContext):
    """  Send a list of form ids and names of its owners to admin
    with inline keyboard of each form id from db  """
    await call.answer(cache_time=1)  # Simple anti-flood
    async with state.proxy() as data:
        db_data = await db.get_forms(begin=data.get("biggest_id_dict"), key="previous")
    logging.info(db_data)
    forms_dict = db_data[0]
    first_row_id = db_data[1]  # ID of the first row in database
    last_row_id = db_data[2]  # ID of the last row in database
    smallest_id_dict = (list(forms_dict.keys()))[-1]  # The smallest ID in dictionary which are 16 rows of database
    biggest_id_dict = (list(forms_dict.keys()))[0]  # The biggest ID in dictionary which are 16 rows of database
    text = ""
    inline_keyboard = types.InlineKeyboardMarkup(row_width=5)
    for key in forms_dict:
        text += f"{key}. {forms_dict[key]}\n"
        button = types.InlineKeyboardButton(text=key, callback_data=key)
        inline_keyboard.insert(button)

    if biggest_id_dict == last_row_id:
        next_button = types.InlineKeyboardButton(text="\U000023ED", callback_data="next")
        inline_keyboard.add(next_button)

    else:
        previous_button = types.InlineKeyboardButton(text="\U000023EE", callback_data="previous")
        next_button = types.InlineKeyboardButton(text="\U000023ED", callback_data="next")
        inline_keyboard.add(previous_button, next_button)

    stats_button = types.InlineKeyboardButton(text="\U0001F4C8 Statistika", callback_data="stats")
    home_button = types.InlineKeyboardButton(text="\U0001F3E0", callback_data="home")
    inline_keyboard.add(stats_button, home_button)
    functions_message = await call.message.edit_text(text, reply_markup=inline_keyboard)
    await state.update_data(sent_forms=[], smallest_id_dict=smallest_id_dict, biggest_id_dict=biggest_id_dict,
                            functions_message_id=functions_message.message_id)


async def send_form(call: types.CallbackQuery, state: FSMContext):
    """  Send a form which admin chose  """
    await call.answer(cache_time=30)  # Simple anti-flood
    form = await db.get_form(call.data)
    form_text = f"<b>Anketa ID:</b> {form['id']}\n" \
                f"<b>Ism va Familiya:</b> {form['full_name']}\n" \
                f"<b>Tug'ulgan sana:</b> {form['birthday']}\n" \
                f"<b>Telefon raqam:</b> +{form['phone_number']}\n" \
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
                f"<b>Telegram ID:</b> {form['user_id']}\n" \
                f"<b>Jo'natilgan sana:</b> {form['date']}\n"

    async with state.proxy() as data:
        smallest_id_dict = data.get("smallest_id_dict")
        biggest_id_dict = data.get("biggest_id_dict")
    db_data = await db.get_forms(begin=smallest_id_dict, end=biggest_id_dict)
    logging.info(db_data)
    forms_dict = db_data[0]
    first_row_id = db_data[1]  # ID of the first row in database
    last_row_id = db_data[2]  # ID of the last row in database
    text = ""
    inline_keyboard = types.InlineKeyboardMarkup(row_width=5)
    for key in forms_dict:
        text += f"{key}. {forms_dict[key]}\n"
        button = types.InlineKeyboardButton(text=key, callback_data=key)
        inline_keyboard.insert(button)
    if not smallest_id_dict == first_row_id:
        next_button = types.InlineKeyboardButton(text="\U000023ED", callback_data="next")
        inline_keyboard.add(next_button)

    if not biggest_id_dict == last_row_id:
        previous_button = types.InlineKeyboardButton(text="\U000023EE", callback_data="previous")
        inline_keyboard.insert(previous_button)

    stats_button = types.InlineKeyboardButton(text="\U0001F4C8 Statistika", callback_data="stats")
    home_button = types.InlineKeyboardButton(text="\U0001F3E0", callback_data="home")
    inline_keyboard.add(stats_button, home_button)

    await call.message.delete()
    form_message = await call.message.answer_photo(photo=form["photo_id"], caption=form_text)
    functions_message = await call.message.answer(text, reply_markup=inline_keyboard)
    async with state.proxy() as data:
        sent_forms = data.get("sent_forms")
        sent_forms.append(form_message.message_id)
        data.update(sent_forms=sent_forms, smallest_id_dict=smallest_id_dict, biggest_id_dict=biggest_id_dict,
                    functions_message_id=functions_message.message_id)


async def send_stats(call: types.CallbackQuery, state: FSMContext):
    """  Send statistics of users and forms received from database using function 'get_stats'  """
    await call.answer(cache_time=3)  # Simple anti-flood
    current_state = await state.get_state()
    async with state.proxy() as data:
        if current_state == "AdminStates:forms":
            sent_forms = data.get('sent_forms')
            for form_id in sent_forms:
                await call.bot.delete_message(chat_id=call.message.chat.id, message_id=form_id)
            await state.finish()

    stats = await db.get_stats()
    functions_message = await call.bot.edit_message_text(text=f"""<b>Statistika:</b>\n
    <b><i>Anketalar:</i></b>\n
    <i>Oxirgi bir kun:</i>      <code>{stats['forms_one_day']}</code>
    <i>Oxirgi bir xafta:</i>   <code>{stats['forms_one_week']}</code>
    <i>Oxirgi bir oy:</i>        <code>{stats['forms_one_month']}</code>
    <i>Oxirgi yarim yil:</i>   <code>{stats['forms_half_year']}</code>
    <i>Oxirgi bir yil:</i>        <code>{stats['forms_one_year']}</code>
    <u><i>Umumiy:</i></u>              <code>{stats['forms_all_time']}</code>\n
    <b><i>Foydalanuvchilar:</i></b>\n
    <i>Oxirgi bir kun:</i>      <code>{stats['users_one_day']}</code>
    <i>Oxirgi bir xafta:</i>   <code>{stats['users_one_week']}</code>
    <i>Oxirgi bir oy:</i>        <code>{stats['users_one_month']}</code>
    <i>Oxirgi yarim yil:</i>   <code>{stats['users_half_year']}</code>
    <i>Oxirgi bir yil:</i>        <code>{stats['users_one_year']}</code>
    <u><i>Umumiy:</i></u>              <code>{stats['users_all_time']}</code>""",
                                                         chat_id=call.message.chat.id,
                                                         message_id=data.get("functions_message_id"),
                                                         reply_markup=admin_function_form_list)
    await state.update_data(functions_message_id=functions_message.message_id)
    await AdminStates.stats.set()


async def go_home(call: types.CallbackQuery, state: FSMContext):
    """  Handle the 'home' button and return to main menu  """
    await call.answer(cache_time=30)  # Simple anti-flood
    current_state = await state.get_state()
    async with state.proxy() as data:
        if current_state == "AdminStates:forms":
            sent_forms = data.get('sent_forms')
            for form_id in sent_forms:
                await call.bot.delete_message(chat_id=call.message.chat.id, message_id=form_id)
        await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get('functions_message_id'))
    await state.finish()
    await call.message.answer("Asosiy menyu!", reply_markup=admin_menu)


def register_admin(dp: Dispatcher):
    dp.register_callback_query_handler(go_home, text_contains="home", state=AdminStates)
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(show_admin_functions, text="\U000026A1", state="*", is_admin=True)
    dp.register_callback_query_handler(send_form_list, text_contains="form_list", state=AdminStates)
    dp.register_callback_query_handler(send_next_form_list, text_contains="next", state=AdminStates.forms)
    dp.register_callback_query_handler(send_previous_form_list, text_contains="previous", state=AdminStates.forms)
    dp.register_callback_query_handler(send_form, regexp="^\d+$", state=AdminStates.forms)
    dp.register_callback_query_handler(send_stats, text_contains="stats", state=AdminStates)
