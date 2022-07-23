import asyncio
import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import MessageCantBeDeleted

from tgbot.keyboards.inline import admin_functions, admin_functions_state_mailing, admin_functions_state_stats, \
    only_confirming_keyboard
from tgbot.keyboards.reply import admin_menu
from tgbot.misc.states import AdminStates
from tgbot.services.database import DBCommands

db = DBCommands("tgbot/db.db")


async def admin_start(message: types.Message, state: FSMContext):
    """  Greet the admin and send an admin menu  """
    await state.finish()
    await message.reply("Xush kelibsiz, Admin!", reply_markup=admin_menu)
    await db.add_user()


async def go_home(call: types.CallbackQuery, state: FSMContext):
    """  Return to main menu  """
    await call.answer(cache_time=1)  # Simple anti-flood
    current_state = await state.get_state()
    async with state.proxy() as data:
        if current_state == "AdminStates:forms":
            sent_forms = data.get('sent_forms')
            for form_id in sent_forms:
                await call.bot.delete_message(chat_id=call.message.chat.id, message_id=form_id)
        try:
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get('functions_message_id'))
        except MessageCantBeDeleted:
            await call.bot.edit_message_text(text="<i>(O'chirilgan xabar)</i>", chat_id=call.message.chat.id,
                                             message_id=data.get("functions_message_id"))
    await call.message.answer("Asosiy menyu!", reply_markup=admin_menu)
    await state.finish()


async def show_admin_functions(message: types.Message, state: FSMContext):
    """  Handle the 'zap' button and direct the admin to the admin mode  """
    await message.answer("Admin Rejimi!", reply_markup=types.ReplyKeyboardRemove())
    functions_message = await message.answer("Mavjud funktsiyalar:", reply_markup=admin_functions)
    await state.update_data(functions_message_id=functions_message.message_id)
    await AdminStates.admin_mode.set()


async def send_form_list(call: types.CallbackQuery, state: FSMContext):
    """  Send a list of form ids and names of its owners to admin
    with inline keyboard of each form id from db  """
    await call.answer(cache_time=1)  # Simple anti-flood

    # Getting forms from database
    db_data = await db.get_forms()
    if db_data is None:
        error_message = await call.message.answer("Ma'lumot mavjud emas!")
        await asyncio.sleep(5)
        await call.bot.delete_message(chat_id=call.message.chat.id, message_id=error_message.message_id)
        return
    forms_dict = db_data[0]
    first_row_id = db_data[1]  # ID of the first row in database
    last_row_id = db_data[2]  # ID of the last row in database
    smallest_id_dict = (list(forms_dict.keys()))[-1]  # The smallest ID in dictionary which are 16 rows of database
    biggest_id_dict = (list(forms_dict.keys()))[0]  # The biggest ID in dictionary which are 16 rows of database

    # Creating a form list with inline keyboard
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
    mailing_button = types.InlineKeyboardButton(text="\U00002709 E'lon berish", callback_data="mailing")
    home_button = types.InlineKeyboardButton(text="\U0001F3E0", callback_data="home")
    inline_keyboard.add(stats_button, mailing_button)
    inline_keyboard.add(home_button)

    # Editing existing message of functions to a new form list and updating data in state
    functions_message = await call.message.edit_text(text, reply_markup=inline_keyboard)
    await state.update_data(sent_forms=[], smallest_id_dict=smallest_id_dict, biggest_id_dict=biggest_id_dict,
                            functions_message_id=functions_message.message_id, first_row_id=first_row_id,
                            last_row_id=last_row_id)
    await AdminStates.forms.set()


async def send_next_form_list(call: types.CallbackQuery, state: FSMContext):
    """  Send the next list of forms  """
    # Getting data from database
    async with state.proxy() as data:
        first_row_id = data.get("first_row_id")
        begin = data.get("smallest_id_dict") - 10
        end = begin + 500
        if begin < first_row_id:
            begin = first_row_id
    db_data = await db.get_forms(begin, end)
    # Getting form list from data in dict type and ordering it in Descending order
    forms_dict = sorted(db_data[0].items(), key=lambda x: x[0], reverse=True)
    forms_dict = {items[0]: items[1] for items in forms_dict}
    smallest_id_dict = (list(forms_dict.keys()))[-1]
    biggest_id_dict = (list(forms_dict.keys()))[0]

    # Creating a form list with inline keyboard
    text = ""
    inline_keyboard = types.InlineKeyboardMarkup(row_width=5)
    for key in forms_dict:
        text += f"{key}. {forms_dict[key]}\n"
        button = types.InlineKeyboardButton(text=key, callback_data=key)
        inline_keyboard.insert(button)

    if smallest_id_dict == first_row_id:
        previous_button = types.InlineKeyboardButton(text="\U000023EE", callback_data="previous")
        inline_keyboard.add(previous_button)

    else:
        previous_button = types.InlineKeyboardButton(text="\U000023EE", callback_data="previous")
        next_button = types.InlineKeyboardButton(text="\U000023ED", callback_data="next")
        inline_keyboard.add(previous_button, next_button)

    stats_button = types.InlineKeyboardButton(text="\U0001F4C8 Statistika", callback_data="stats")
    mailing_button = types.InlineKeyboardButton(text="\U00002709 E'lon berish", callback_data="mailing")
    home_button = types.InlineKeyboardButton(text="\U0001F3E0", callback_data="home")
    inline_keyboard.add(stats_button, mailing_button)
    inline_keyboard.add(home_button)

    # Editing existing message of form list to a new form list and updating data in state
    functions_message = await call.message.edit_text(text, reply_markup=inline_keyboard)
    await state.update_data(smallest_id_dict=smallest_id_dict, biggest_id_dict=biggest_id_dict,
                            functions_message_id=functions_message.message_id)


async def send_previous_form_list(call: types.CallbackQuery, state: FSMContext):
    """  Send the previous list of forms  """
    # Getting forms from database
    async with state.proxy() as data:
        last_row_id = data.get("last_row_id")
        begin = data.get("biggest_id_dict") + 1
        end = begin + 9
        if end > last_row_id:
            end = last_row_id
            begin = end - 10
    db_data = await db.get_forms(begin, end)
    # Getting form list from data in dict type and ordering it in Descending order
    forms_dict = sorted(db_data[0].items(), key=lambda x: x[0], reverse=True)
    forms_dict = {items[0]: items[1] for items in forms_dict}
    smallest_id_dict = (list(forms_dict.keys()))[-1]
    biggest_id_dict = (list(forms_dict.keys()))[0]

    # Creating a form list with inline keyboard
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
    mailing_button = types.InlineKeyboardButton(text="\U00002709 E'lon berish", callback_data="mailing")
    home_button = types.InlineKeyboardButton(text="\U0001F3E0", callback_data="home")
    inline_keyboard.add(stats_button, mailing_button)
    inline_keyboard.add(home_button)

    # Editing existing message of form list to a new form list and updating data in state
    functions_message = await call.message.edit_text(text, reply_markup=inline_keyboard)
    await state.update_data(smallest_id_dict=smallest_id_dict, biggest_id_dict=biggest_id_dict,
                            functions_message_id=functions_message.message_id)


async def send_form(call: types.CallbackQuery, state: FSMContext):
    """  Send a form which admin chose  """
    await call.answer(cache_time=5)  # Simple anti-flood

    # Making form's text
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

    # Getting forms from database
    async with state.proxy() as data:
        smallest_id_dict = data.get("smallest_id_dict")
        biggest_id_dict = data.get("biggest_id_dict")
    db_data = await db.get_forms(begin=smallest_id_dict, end=biggest_id_dict)
    # Getting form list from data in dict type and ordering it in Descending order
    forms_dict = sorted(db_data[0].items(), key=lambda x: x[0], reverse=True)
    forms_dict = {items[0]: items[1] for items in forms_dict}
    first_row_id = db_data[1]  # ID of the first row in database
    last_row_id = db_data[2]  # ID of the last row in database

    # Creating a form list with inline keyboard
    text = ""
    inline_keyboard = types.InlineKeyboardMarkup(row_width=5)
    for key in forms_dict:
        text += f"{key}. {forms_dict[key]}\n"
        button = types.InlineKeyboardButton(text=key, callback_data=key)
        inline_keyboard.insert(button)

    if smallest_id_dict == first_row_id and biggest_id_dict != last_row_id:
        previous_button = types.InlineKeyboardButton(text="\U000023EE", callback_data="previous")
        inline_keyboard.add(previous_button)

    elif biggest_id_dict == last_row_id and smallest_id_dict != first_row_id:
        next_button = types.InlineKeyboardButton(text="\U000023ED", callback_data="next")
        inline_keyboard.add(next_button)

    elif smallest_id_dict != first_row_id and biggest_id_dict != last_row_id:
        previous_button = types.InlineKeyboardButton(text="\U000023EE", callback_data="previous")
        next_button = types.InlineKeyboardButton(text="\U000023ED", callback_data="next")
        inline_keyboard.add(previous_button, next_button)

    stats_button = types.InlineKeyboardButton(text="\U0001F4C8 Statistika", callback_data="stats")
    mailing_button = types.InlineKeyboardButton(text="\U00002709 E'lon berish", callback_data="mailing")
    home_button = types.InlineKeyboardButton(text="\U0001F3E0", callback_data="home")
    inline_keyboard.add(stats_button, mailing_button)
    inline_keyboard.add(home_button)

    # Sending form with inline keyboard
    await call.message.delete()
    form_message = await call.message.answer_photo(photo=form["photo_id"], caption=form_text)
    functions_message = await call.message.answer(text, reply_markup=inline_keyboard)
    async with state.proxy() as data:
        sent_forms = data.get("sent_forms")
        sent_forms.append(form_message.message_id)
        data.update(sent_forms=sent_forms, functions_message_id=functions_message.message_id)


async def send_stats(call: types.CallbackQuery, state: FSMContext):
    """  Send statistics of users and forms received from database using function 'get_stats'  """
    await call.answer(cache_time=1)  # Simple anti-flood
    current_state = await state.get_state()
    async with state.proxy() as data:
        if current_state == "AdminStates:forms":
            sent_forms = data.get('sent_forms')
            for form_id in sent_forms:
                await call.bot.delete_message(chat_id=call.message.chat.id, message_id=form_id)
            await state.finish()

    stats = await db.get_stats()
    # Do not remove the whitespaces!!!
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
                                                         reply_markup=admin_functions_state_stats)
    await state.update_data(functions_message_id=functions_message.message_id)
    await AdminStates.stats.set()


async def mailing_start(call: types.CallbackQuery, state: FSMContext):
    """  Start mailing to users. Ask the admin to write the mail text  """
    await call.answer(cache_time=1)  # Simple anti-flood
    current_state = await state.get_state()
    async with state.proxy() as data:
        if current_state == "AdminStates:forms":
            sent_forms = data.get('sent_forms')
            for form_id in sent_forms:
                await call.bot.delete_message(chat_id=call.message.chat.id, message_id=form_id)
        await call.bot.edit_message_text(text="<b>Jo'natmoqchi bo'lgan xabaringizni yozing!</b>\n",
                                         chat_id=call.message.chat.id, message_id=data.get("functions_message_id"),
                                         reply_markup=admin_functions_state_mailing)
    await AdminStates.mailing_start.set()


async def mailing_confirm(message: types.Message, state: FSMContext):
    """  Ask the admin to confirm the mailing  """
    await message.delete()
    copied_message = await message.send_copy(chat_id=message.chat.id)
    await message.answer(text="<b>Ushbu xabarni barchaga jo'natishga rozimisiz?</b>",
                                             reply_markup=only_confirming_keyboard)
    await state.update_data(copied_message_id=copied_message.message_id)
    await AdminStates.mailing_confirm.set()


async def callback_no(call: types.CallbackQuery, state: FSMContext):
    """  Return to admin mode  """
    await call.answer(cache_time=1)  # Simple anti-flood
    async with state.proxy() as data:
        await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get("copied_message_id"))
    await state.finish()
    functions_message = await call.message.edit_text("Mavjud funcktsiyalar:", reply_markup=admin_functions)
    await AdminStates.admin_mode.set()
    await state.update_data(functions_message_id=functions_message.message_id)


async def send_mail(call: types.CallbackQuery, state: FSMContext):
    """  Send the mail to all users in database  """
    try:
        user_ids = await db.get_all_users()
        data = await state.get_data()
        copied_message_id = data.get("copied_message_id")
        for user_id in user_ids:
            if user_id[0] == call.message.chat.id:
                continue

            await call.bot.copy_message(chat_id=user_id[0], from_chat_id=call.message.chat.id,
                                        message_id=copied_message_id)
    except Exception as error:
        await call.answer(f"Xato! Dasturchiga murojat qiling!\n{error}", show_alert=True)
        await call.message.edit_text("Mavjud funktsiyalar:", reply_markup=admin_functions)
        await AdminStates.admin_mode.set()
    else:
        await call.message.edit_reply_markup()
        functions_message = await call.message.answer("E'lon muvaffaqiyatli jo'natildi! \U0001F389",
                                                      reply_markup=admin_functions)
        await state.finish()
        await state.update_data(functions_message_id=functions_message.message_id)
        await AdminStates.admin_mode.set()


def register_admin(dp: Dispatcher):
    dp.register_callback_query_handler(go_home, text_contains="home", state=AdminStates)
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(show_admin_functions, text="\U000026A1", state="*", is_admin=True)
    dp.register_callback_query_handler(send_form_list, text_contains="form_list", state=AdminStates)
    dp.register_callback_query_handler(send_next_form_list, text_contains="next", state=AdminStates.forms)
    dp.register_callback_query_handler(send_previous_form_list, text_contains="previous", state=AdminStates.forms)
    dp.register_callback_query_handler(send_form, regexp="^\d+$", state=AdminStates.forms)
    dp.register_callback_query_handler(send_stats, text_contains="stats", state=AdminStates)
    dp.register_callback_query_handler(mailing_start, text_contains="mailing", state=AdminStates)
    dp.register_message_handler(mailing_confirm, content_types=types.ContentType.ANY, state=AdminStates.mailing_start)
    dp.register_callback_query_handler(callback_no, text_contains="no", state=AdminStates.mailing_confirm)
    dp.register_callback_query_handler(send_mail, text_contains="yes", state=AdminStates.mailing_confirm)
