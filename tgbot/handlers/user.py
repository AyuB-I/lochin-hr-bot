import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext, BaseStorage

from tgbot.keyboards.reply import menu_keyboard, cancel_form_button, form_keyboard, phonenum_keyboard
from tgbot.keyboards.inline import confirming_keyboard, professions_keyboard, fill_form_keyboard
from tgbot.misc.states import FormStates


async def user_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Assalamu Alaykum!\n\"Lochin Mould\" korxonasinig anketa to'ldirish botiga xush kelibsiz !!!",
                         reply_markup=menu_keyboard)


async def about_us(message: types.Message):
    await message.answer("Quyidagi xavola orqali \"Lochin Mould\" korxonasining faoliyati haqida to'liq ma'lumotga "
                         "ega bo'lishingiz mumkin.\n"
                         "@Lochin_MouldBot")


async def cancel_form(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Ro'yhatdan o'tish bekor qilindi!", reply_markup=menu_keyboard)


async def ask_q1(message: types.Message):
    await message.answer("Ism va familiyangizni to'liq kiriting.\n(Ahmadjon Ahmedov)",
                         reply_markup=cancel_form_button)
    await FormStates.q1_name.set()


async def ask_q2(message: types.Message, state: FSMContext):
    await message.answer("Tug'ulgan sanangizni kiriting.\n(24.03.1998)", reply_markup=form_keyboard)
    if message.text != "\U00002B05 Orqaga":
        await state.update_data(full_name=message.text.title())  # !!!Tutuq belgizidan keyingiz xarfni kottalashtiryapti
    await FormStates.q2_birthdate.set()


async def ask_q3(message: types.Message, state: FSMContext):
    await message.answer("Siz bilan bog'lanishimiz mumkin bo'lgan telefon raqamni kiriting.\n(+998916830071)",
                         reply_markup=phonenum_keyboard)
    await state.update_data(bithdate=message.text)
    async with state.proxy() as data:
        logging.info(data.get("full_name"))
    await FormStates.q3_phonenum.set()


async def ask_q3_callback(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    async with state.proxy() as data:
        await call.bot.delete_message(chat_id, data.get("q4_id"))
        logging.info(data.get("full_name"))
    await call.message.answer("Siz bilan bog'lanishimiz mumkin bo'lgan telefon raqamni kiriting.\n(+998916830071)",
                              reply_markup=phonenum_keyboard)
    await FormStates.q3_phonenum.set()


async def confirm_q3(message: types.Message, state: FSMContext):
    if message.text and message.text != "\U00002B05 Orqaga":
        phonenum = message.text
    else:
        phonenum = message.contact.phone_number
    msg_1 = await message.answer(f"Raqamni to'g'ri terdingizmi?", reply_markup=cancel_form_button)
    msg_2 = await message.answer(phonenum, reply_markup=confirming_keyboard)
    await state.update_data(phonenum=phonenum, confirm_q3_id_1=msg_1.message_id, confirm_q3_id_2=msg_2.message_id)


async def callback_no(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    async with state.proxy() as data:
        await call.bot.delete_message(chat_id, data.get("confirm_q3_id_2"))
        await call.bot.delete_message(chat_id, data.get("confirm_q3_id_1"))
    await call.message.answer("Siz bilan bog'lanishimiz mumkin bo'lgan telefon raqamni kiriting.\n(+998916830071)",
                              reply_markup=phonenum_keyboard)


async def ask_q4(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    if call.data == "yes":
        async with state.proxy() as data:
            await call.bot.delete_message(chat_id, data.get("confirm_q3_id_2"))
            await call.bot.delete_message(chat_id, data.get("confirm_q3_id_1"))
        await call.message.answer("Ma'lumotlar qabul qilindi!", reply_markup=cancel_form_button)
    else:
        async with state.proxy() as data:
            await call.bot.delete_message(chat_id, data.get("profession_text_id_2"))
            await call.bot.delete_message(chat_id, data.get("profession_text_id_1"))

    msg = await call.message.answer("Sohangiz bo'yicha yo'nalishni tanlang.", reply_markup=professions_keyboard)
    await state.update_data(q4_id=msg.message_id)
    await FormStates.q4_profession.set()
    async with state.proxy() as data:
        logging.info(data.get("phonenum"))


async def callback_sales_manager(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    async with state.proxy() as data:
        await call.bot.delete_message(chat_id, data.get("q4_id"))
    await state.update_data(profession="Sotuv menejer bo'limi")
    msg_1 = await call.message.answer("Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.",
                              reply_markup=form_keyboard)
    msg_2 = await call.message.answer("Tanishib chiqqaningizdan so'ng anketa to'ldirishingiz mumkin.",
                              reply_markup=fill_form_keyboard)
    await state.update_data(profession_text_id_1=msg_1.message_id, profession_text_id_2=msg_2.message_id)
    await FormStates.starting_next_form.set()


async def callback_advertising(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    async with state.proxy() as data:
        await call.bot.delete_message(chat_id, data.get("q4_id"))
    msg_1 = await call.message.answer("Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.",
                              reply_markup=cancel_form_button)
    msg_2 = await call.message.answer("Tanishib chiqqaningizdan so'ng anketa to'ldirishingiz mumkin.",
                              reply_markup=fill_form_keyboard)
    await state.update_data(profession="Reklama bo'limi")
    await state.update_data(profession_text_id_1=msg_1.message_id, profession_text_id_2=msg_2.message_id)
    await FormStates.starting_next_form.set()


async def callback_finance(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    async with state.proxy() as data:
        await call.bot.delete_message(chat_id, data.get("q4_id"))
    await state.update_data(profession="Moliya bo'limi")
    msg_1 = await call.message.answer("Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.",
                              reply_markup=cancel_form_button)
    msg_2 = await call.message.answer("Tanishib chiqqaningizdan so'ng anketa to'ldirishingiz mumkin.",
                              reply_markup=fill_form_keyboard)
    await state.update_data(profession_text_id_1=msg_1.message_id, profession_text_id_2=msg_2.message_id)
    await FormStates.starting_next_form.set()


async def callback_hr(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    async with state.proxy() as data:
        await call.bot.delete_message(chat_id, data.get("q4_id"))
    await state.update_data(profession="Kadrlar bo'limi")
    msg_1 = await call.message.answer("Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.",
                              reply_markup=cancel_form_button)
    msg_2 = await call.message.answer("Tanishib chiqqaningizdan so'ng anketa to'ldirishingiz mumkin.",
                              reply_markup=fill_form_keyboard)
    await state.update_data(profession_text_id_1=msg_1.message_id, profession_text_id_2=msg_2.message_id)
    await FormStates.starting_next_form.set()


async def callback_accounting(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    async with state.proxy() as data:
        await call.bot.delete_message(chat_id, data.get("q4_id"))
    await state.update_data(profession="Buxgalteriya bo'limi")
    msg_1 = await call.message.answer("Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.",
                              reply_markup=cancel_form_button)
    msg_2 = await call.message.answer("Tanishib chiqqaningizdan so'ng anketa to'ldirishingiz mumkin.",
                              reply_markup=fill_form_keyboard)
    await state.update_data(profession_text_id_1=msg_1.message_id, profession_text_id_2=msg_2.message_id)
    await FormStates.starting_next_form.set()


async def callback_marketing(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    async with state.proxy() as data:
        await call.bot.delete_message(chat_id, data.get("q4_id"))
    await state.update_data(profession="Marketing bo'limi")
    msg_1 = await call.message.answer("Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.",
                              reply_markup=cancel_form_button)
    msg_2 = await call.message.answer("Tanishib chiqqaningizdan so'ng anketa to'ldirishingiz mumkin.",
                              reply_markup=fill_form_keyboard)
    await state.update_data(profession_text_id_1=msg_1.message_id, profession_text_id_2=msg_2.message_id)
    await FormStates.starting_next_form.set()


async def ask_q5(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.message.answer("Yashash manzilingiz.\n(Qo'qon shahar, Imom Buxoriy 42)", reply_markup=form_keyboard)
    await FormStates.q5_address.set()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(cancel_form, text_contains="Bekor qilish", state="*")
    dp.register_message_handler(about_us, text_contains="Korxona haqida")
    dp.register_message_handler(ask_q1, text_contains="Ro'yhatdan o'tish")
    dp.register_message_handler(ask_q2, regexp=("^[a-zA-Z']{3,}\s[a-zA-Z']{3,}$"), state=FormStates.q1_name)
    dp.register_message_handler(ask_q1, text_contains="\U00002B05 Orqaga", state=FormStates.q2_birthdate)
    dp.register_message_handler(ask_q3, regexp=("^\d{1,2}\.\d{2}\.[12][90][06-9]\d$"),
                                state=FormStates.q2_birthdate)
    dp.register_message_handler(ask_q2, text_contains="\U00002B05 Orqaga", state=FormStates.q3_phonenum)
    dp.register_message_handler(confirm_q3, regexp=("^\+998[0-9]{9}$"), state=FormStates.q3_phonenum)
    dp.register_message_handler(confirm_q3, content_types=types.ContentTypes.CONTACT,
                                state=FormStates.q3_phonenum)
    dp.register_callback_query_handler(callback_no, text_contains="no", state=FormStates.q3_phonenum)
    dp.register_callback_query_handler(ask_q4, text_contains="yes", state=FormStates.q3_phonenum)
    dp.register_callback_query_handler(ask_q3_callback, text_contains="back", state=FormStates.q4_profession)
    dp.register_callback_query_handler(callback_sales_manager, text_contains="sales_manager",
                                       state=FormStates.q4_profession)
    dp.register_callback_query_handler(callback_advertising, text_contains="advertising",
                                       state=FormStates.q4_profession)
    dp.register_callback_query_handler(callback_finance, text_contains="finance", state=FormStates.q4_profession)
    dp.register_callback_query_handler(callback_hr, text_contains="hr", state=FormStates.q4_profession)
    dp.register_callback_query_handler(callback_accounting, text_contains="accounting", state=FormStates.q4_profession)
    dp.register_callback_query_handler(callback_marketing, text_contains="marketing", state=FormStates.q4_profession)
    dp.register_callback_query_handler(ask_q5, text_contains="fill_form", state=FormStates.starting_next_form)
    dp.register_callback_query_handler(ask_q4, text_contains="back", state=FormStates.starting_next_form)
