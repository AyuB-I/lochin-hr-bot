import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext, BaseStorage

from tgbot.keyboards.reply import menu_keyboard, cancel_form_button, form_keyboard, phonenum_keyboard
from tgbot.keyboards.inline import confirming_keyboard, professions_keyboard, fill_form_keyboard
from tgbot.misc.states import PrivateForm, ProfessionForm


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


async def ask_private_q1(message: types.Message):
    await message.answer("Ism va familiyangizni to'liq kiriting.\n(Ahmadjon Ahmedov)",
                         reply_markup=cancel_form_button)
    await PrivateForm.q1_name.set()


async def ask_private_q2(message: types.Message, state: FSMContext):
    await message.answer("Tug'ulgan sanangizni kiriting.\n(24.03.1998)", reply_markup=form_keyboard)
    if message.text != "\U00002B05 Orqaga":
        await state.update_data(full_name=message.text.title())  # !!!Tutuq belgizidan keyingiz xarfni kottalashtiryapti
    await PrivateForm.q2_birthdate.set()


async def ask_private_q3(message: types.Message, state: FSMContext):
    if message.text != "\U00002B05 Orqaga":
        await state.update_data(bithdate=message.text)
    await message.answer("Siz bilan bog'lanishimiz mumkin bo'lgan telefon raqamni kiriting.\n(+998916830071)",
                         reply_markup=phonenum_keyboard)
    async with state.proxy() as data:
        logging.info(data.get("full_name"))
    await PrivateForm.q3_phonenum.set()


async def confirm_private_q3(message: types.Message, state: FSMContext):
    if message.text and message.text != "\U00002B05 Orqaga":
        phonenum = message.text
    else:
        phonenum = f"+{message.contact.phone_number}"
    await state.update_data(phonenum=phonenum)
    await message.answer(f"Raqamni to'g'ri terdingizmi?", reply_markup=cancel_form_button)
    await message.answer(phonenum, reply_markup=confirming_keyboard)


async def callback_no(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer("Siz bilan bog'lanishimiz mumkin bo'lgan telefon raqamni kiriting.\n(+998916830071)",
                              reply_markup=phonenum_keyboard)


async def ask_private_q4(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.message.answer("Malumotlar qabul qilindi!", reply_markup=form_keyboard)
    await call.message.answer("Sohangiz bo'yicha yo'nalishni tanlang.", reply_markup=professions_keyboard)
    await PrivateForm.q4_profession.set()
    async with state.proxy() as data:
        logging.info(data.get("phonenum"))


async def back_to_q4(message: types.Message):
    await message.answer("Sohangiz bo'yicha yo'nalishni tanlang.", reply_markup=professions_keyboard)
    await PrivateForm.q4_profession.set()


async def callback_sales_manager(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await state.update_data(profession="Sotuv menejer bo'limi")
    await call.message.answer("Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.\n"
                              "Tanishib chiqqaningizdan so'ng anketa to'ldirishingiz mumkin.",
                              reply_markup=fill_form_keyboard)
    await ProfessionForm.starting_form.set()


async def callback_advertising(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await state.update_data(profession="Reklama bo'limi")
    await call.message.answer("Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.\n"
                              "Tanishib chiqqaningizdan so'ng anketa to'ldirishingiz mumkin.",
                              reply_markup=fill_form_keyboard)
    await ProfessionForm.starting_form.set()


async def callback_finance(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await state.update_data(profession="Moliya bo'limi")
    await call.message.answer("Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.\n"
                              "Tanishib chiqqaningizdan so'ng anketa to'ldirishingiz mumkin.",
                              reply_markup=fill_form_keyboard)
    await ProfessionForm.starting_form.set()


async def callback_hr(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await state.update_data(profession="Kadrlar bo'limi")
    await call.message.answer("Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.\n"
                              "Tanishib chiqqaningizdan so'ng anketa to'ldirishingiz mumkin.",
                              reply_markup=fill_form_keyboard)
    await ProfessionForm.starting_form.set()


async def callback_accounting(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await state.update_data(profession="Buxgalteriya bo'limi")
    await call.message.answer("Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.\n"
                              "Tanishib chiqqaningizdan so'ng anketa to'ldirishingiz mumkin.",
                              reply_markup=fill_form_keyboard)
    await ProfessionForm.starting_form.set()


async def callback_marketing(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await state.update_data(profession="Marketing bo'limi")
    await call.message.answer("Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.\n"
                              "Tanishib chiqqaningizdan so'ng anketa to'ldirishingiz mumkin.",
                              reply_markup=fill_form_keyboard)
    await ProfessionForm.starting_form.set()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(cancel_form, text_contains="Bekor qilish", state="*")
    dp.register_message_handler(about_us, text_contains="Korxona haqida")
    dp.register_message_handler(ask_private_q1, text_contains="Ro'yhatdan o'tish")
    dp.register_message_handler(ask_private_q2, regexp=("^[a-zA-Z']{3,}\s[a-zA-Z']{3,}$"), state=PrivateForm.q1_name)
    dp.register_message_handler(ask_private_q1, text_contains="\U00002B05 Orqaga", state=PrivateForm.q2_birthdate)
    dp.register_message_handler(ask_private_q3, regexp=("^\d{1,2}\.\d{2}\.[12][90][06-9]\d$"),
                                state=PrivateForm.q2_birthdate)
    dp.register_message_handler(ask_private_q2, text_contains="\U00002B05 Orqaga", state=PrivateForm.q3_phonenum)
    dp.register_message_handler(confirm_private_q3, regexp=("\+998[0-9]{9}?"), state=PrivateForm.q3_phonenum)
    dp.register_message_handler(confirm_private_q3, content_types=types.ContentTypes.CONTACT,
                                state=PrivateForm.q3_phonenum)
    dp.register_callback_query_handler(callback_no, text_contains="no", state=PrivateForm.q3_phonenum)
    dp.register_callback_query_handler(ask_private_q4, text_contains="yes", state=PrivateForm.q3_phonenum)
    dp.register_message_handler(ask_private_q3, text_contains="\U00002B05 Orqaga", state=PrivateForm.q4_profession)
    dp.register_message_handler(back_to_q4, text_contains="\U00002B05 Orqaga", state=ProfessionForm.starting_form)
    dp.register_callback_query_handler(callback_sales_manager, text_contains="sales_manager",
                                       state=PrivateForm.q4_profession)
    dp.register_callback_query_handler(callback_advertising, text_contains="advertising",
                                       state=PrivateForm.q4_profession)
    dp.register_callback_query_handler(callback_finance, text_contains="finance", state=PrivateForm.q4_profession)
    dp.register_callback_query_handler(callback_hr, text_contains="hr", state=PrivateForm.q4_profession)
    dp.register_callback_query_handler(callback_accounting, text_contains="accounting", state=PrivateForm.q4_profession)
    dp.register_callback_query_handler(callback_marketing, text_contains="marketing", state=PrivateForm.q4_profession)
