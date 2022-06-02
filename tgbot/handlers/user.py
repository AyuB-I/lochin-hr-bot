from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import MessageIdentifierNotSpecified, MessageToDeleteNotFound

from tgbot.config import Config
from tgbot.keyboards.inline import confirming_keyboard, professions_keyboard, fill_form_keyboard, nations_keyboard, \
    edu_keyboard, marital_status_keyboard, license_keyboard, level_keyboard, origin_keyboard, sending_keyboard
from tgbot.keyboards.reply import menu_keyboard, cancel_form_button, form_keyboard, phonenum_keyboard
from tgbot.misc.states import FormStates
from tgbot.services.database import DBCommands


db = DBCommands("tgbot\db.db")


async def user_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Assalamu Alaykum!\n\"Lochin Mould\" korxonasinig anketa to'ldirish botiga xush kelibsiz !!!",
                         reply_markup=menu_keyboard)
    await db.register_user()


async def about_us(message: types.Message):
    await message.answer("Quyidagi xavola orqali \"Lochin Mould\" korxonasining faoliyati haqida to'liq ma'lumotga "
                         "ega bo'lishingiz mumkin.\n"
                         "@Lochin_MouldBot")


async def incorrect_answer(message: types.Message):
    await message.delete()
    await message.answer("<b>Noto'g'ri ma'lumot kiritdingiz!</b>\n"
                         "Iltimos, ma'lumotlarni ko'rsatilgan shakilda kiriting.")


async def cancel_form(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Ro'yhatdan o'tish bekor qilindi!", reply_markup=menu_keyboard)


async def ask_q1(message: types.Message, state: FSMContext):
    if message.text == "\U00002B05 Orqaga":
        await message.delete()
    await message.answer("<b>Ism va familiyangizni to'liq kiriting.</b>\n(Ahmadjon Ahmedov)",
                         reply_markup=cancel_form_button)
    await FormStates.q1_name.set()


async def ask_q2(message: types.Message, state: FSMContext):
    if message.text != "\U00002B05 Orqaga":
        chat_id = message.chat.id
        await state.update_data(full_name=message.text.title())  # !!!Tutuq belgizidan keyingiz xarfni kottalashtiryapti
    elif message.text == "\U00002B05 Orqaga":
        await message.delete()
    await message.answer("<b>Tug'ulgan sanangizni kiriting.</b>\n(24.03.1998)", reply_markup=form_keyboard)
    await FormStates.q2_birthdate.set()


async def ask_q3(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    if message.text == "\U00002B05 Orqaga":
        await message.delete()
    await message.answer("<b>Siz bilan bog'lanishimiz mumkin bo'lgan telefon raqamni kiriting.</b>\n(+998916830071)",
                         reply_markup=phonenum_keyboard)
    await state.update_data(birthdate=message.text)
    await FormStates.q3_phonenum.set()


async def ask_q3_callback(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    async with state.proxy() as data:
        await call.bot.delete_message(chat_id, data.get("q4_id"))
    await call.message.answer(
        "<b>Siz bilan bog'lanishimiz mumkin bo'lgan telefon raqamni kiriting.</b>\n(+998916830071)",
        reply_markup=phonenum_keyboard)
    await FormStates.q3_phonenum.set()


async def confirm_q3(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    if message.text and message.text != "\U00002B05 Orqaga":
        phonenum = message.text
    else:
        phonenum = message.contact.phone_number
    msg_1 = await message.answer(f"<b>Raqamni to'g'ri terdingizmi?</b>", reply_markup=cancel_form_button)
    msg_2 = await message.answer(phonenum, reply_markup=confirming_keyboard)
    await state.update_data(phonenum=phonenum, confirm_q3_id_1=msg_1.message_id, confirm_q3_id_2=msg_2.message_id)


async def callback_no(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    async with state.proxy() as data:
        await call.bot.delete_message(chat_id, data.get("confirm_q3_id_2"))
        await call.bot.delete_message(chat_id, data.get("confirm_q3_id_1"))
    await call.message.answer(
        "<b>Siz bilan bog'lanishimiz mumkin bo'lgan telefon raqamni kiriting.</b>\n(+998916830071)",
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

    msg = await call.message.answer("<b>Sohangiz bo'yicha yo'nalishni tanlang.</b>", reply_markup=professions_keyboard)
    await state.update_data(q4_id=msg.message_id)
    await FormStates.q4_profession.set()


async def ask_q4_message(message: types.Message, state: FSMContext):
    msg = await message.answer("<b>Sohangiz bo'yicha yo'nalishni tanlang.</b>", reply_markup=professions_keyboard)
    await state.update_data(q4_id=msg.message_id)
    await FormStates.q4_profession.set()


async def callback_sales_manager(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    async with state.proxy() as data:
        await call.bot.delete_message(chat_id, data.get("q4_id"))
    await state.update_data(profession="Savdo menejment bo'limi")
    msg_1 = await call.message.answer_photo(
        photo="AgACAgIAAxkBAAIVFGJ6X9tyHAplodTrvc3dilrUS_8XAAL6ujEbqufZS8YKYJnCRxLQAQADAgADeQADJAQ",
        caption="<b>Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.</b>",
        reply_markup=cancel_form_button)
    msg_2 = await call.message.answer("Tanishib chiqqaningizdan so'ng anketa to'ldirishingiz mumkin.",
                                      reply_markup=fill_form_keyboard)
    await state.update_data(profession_text_id_1=msg_1.message_id, profession_text_id_2=msg_2.message_id)
    await FormStates.starting_next_form.set()


async def callback_advertising(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    async with state.proxy() as data:
        await call.bot.delete_message(chat_id, data.get("q4_id"))
    msg_1 = await call.message.answer_photo(
        photo="AgACAgIAAxkBAAIVFmJ6X-jOYfNFOdNzGcwRta7Z_H04AAIKuzEbqufZSz67gDQxaVAnAQADAgADeQADJAQ",
        caption="<b>Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.</b>",
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
    msg_1 = await call.message.answer_photo(
        photo="AgACAgIAAxkBAAIVGGJ6X_kDiUAfCTe_JiwTCvMd4TqfAAILuzEbqufZS3cTHo3jopF0AQADAgADeQADJAQ",
        caption="<b>Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.</b>",
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
    msg_1 = await call.message.answer_photo(
        photo="AgACAgIAAxkBAAIVGmJ6YAZ1-c2aSCYZ5CpbXtPm8H4RAAIMuzEbqufZS8KQIUte4l7MAQADAgADeQADJAQ",
        caption="<b>Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.</b>",
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
    msg_1 = await call.message.answer_photo(
        photo="AgACAgIAAxkBAAIVHGJ6YAwt1eEQ56oZSDGUBOjklGv1AAINuzEbqufZS-shHsLBIonWAQADAgADeQADJAQ",
        caption="<b>Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.</b>",
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
    msg_1 = await call.message.answer_photo(
        photo="AgACAgIAAxkBAAIVHmJ6YBC2QUOYaoWVv1lomU1gHuqJAAIOuzEbqufZSycrKMsuQ89mAQADAgADeQADJAQ",
        caption="<b>Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.</b>",
        reply_markup=cancel_form_button)
    msg_2 = await call.message.answer("Tanishib chiqqaningizdan so'ng anketa to'ldirishingiz mumkin.",
                                      reply_markup=fill_form_keyboard)
    await state.update_data(profession_text_id_1=msg_1.message_id, profession_text_id_2=msg_2.message_id)
    await FormStates.starting_next_form.set()


async def ask_q5(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    address_mes = await call.message.answer("<b>Yashash manzilingiz.</b>\n(Qo'qon shahar, Imom Buxoriy 42)",
                                            reply_markup=form_keyboard)
    await state.update_data(address_mes_id=address_mes.message_id)
    await FormStates.q5_address.set()


async def ask_q5_message(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        await message.bot.delete_message(chat_id, data.get("nation_mes_id"))
    await message.delete()
    address_mes = await message.answer("<b>Yashash manzilingiz.</b>\n(Qo'qon shahar, Imom Buxoriy 42)")
    await state.update_data(address_mes_id=address_mes.message_id)
    await FormStates.q5_address.set()


async def ask_q6(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    if message.text != "\U00002B05 Orqaga":
        await state.update_data(address=message.text)
    await message.delete()
    async with state.proxy() as data:
        try:
            await message.bot.delete_message(chat_id, data.get("address_mes_id"))
        except MessageToDeleteNotFound:
            pass
        try:
            await message.bot.delete_message(chat_id, data.get("edu_mes_id"))
        except MessageIdentifierNotSpecified:
            await message.answer(f"<b>Yashash manzil:</b>\n{data.get('address')}", reply_markup=form_keyboard)
        except MessageToDeleteNotFound:
            await message.answer(f"<b>Yashash manzil:</b>\n{data.get('address')}", reply_markup=form_keyboard)

    nation_mes = await message.answer("<b>Millatingiz:</b>", reply_markup=nations_keyboard)
    await state.update_data(nation_mes_id=nation_mes.message_id)
    await FormStates.q6_nation.set()


async def ask_q7(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    if call.data == "uz":
        await state.update_data(nation="O'zbek")
    elif call.data == "ru":
        await state.update_data(nation="Rus")
    else:
        await state.update_data(nation="Boshqa")
    async with state.proxy() as data:
        await call.message.edit_text(f"<b>Millat:</b>\n{data.get('nation')}")
    edu_mes = await call.message.answer("<b>Ma'lumotingiz:</b>", reply_markup=edu_keyboard)
    await state.update_data(edu_mes_id=edu_mes.message_id)
    await FormStates.q7_edu.set()


async def ask_q7_message(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        await message.bot.delete_message(chat_id, data.get("marital_mes_id"))
    await message.delete()
    edu_mes = await message.answer("<b>Ma'lumotingiz:</b>", reply_markup=edu_keyboard)
    await state.update_data(edu_mes_id=edu_mes.message_id)
    await FormStates.q7_edu.set()


async def ask_q8(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    if call.data == "secondary":
        await state.update_data(edu="O'rta")
    elif call.data == "secondary_special":
        await state.update_data(edu="O'rta maxsus")
    elif call.data == "bachalor":
        await state.update_data(edu="Oliy | Bakalavr")
    else:
        await state.update_data(edu="Oliy | Magistr")

    async with state.proxy() as data:
        await call.message.edit_text(f"<b>Ma'lumot:</b>\n{data.get('edu')}")
    marital_mes = await call.message.answer("<b>Oilaviy ahvolingiz:</b>", reply_markup=marital_status_keyboard)
    await state.update_data(marital_mes_id=marital_mes.message_id)
    await FormStates.q8_marital_status.set()


async def ask_q8_message(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        await message.bot.delete_message(chat_id, data.get("trip_mes_id"))
    await message.delete()
    marital_mes = await message.answer("<b>Oilaviy ahvolingiz:</b>", reply_markup=marital_status_keyboard)
    await state.update_data(marital_mes_id=marital_mes.message_id)
    await FormStates.q8_marital_status.set()


async def ask_q9(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    if call.data == "married":
        await state.update_data(marital_status="Turmush qurgan")
    else:
        await state.update_data(marital_status="Turmush qurmagan")

    async with state.proxy() as data:
        await call.message.edit_text(f"<b>Oilaviy ahvol:</b>\n{data.get('marital_status')}")
    trip_mes = await call.message.answer("<b>Korxona tomonidan xizmat safariga chiqishga rozimisiz?</b>",
                                         reply_markup=confirming_keyboard)
    await state.update_data(trip_mes_id=trip_mes.message_id)
    await FormStates.q9_trip.set()


async def ask_q9_message(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        await message.bot.delete_message(chat_id, data.get("military_mes_id"))
    await message.delete()
    trip_mes = await message.answer("<b>Korxona tomonidan xizmat safariga chiqishga rozimisiz?</b>",
                                    reply_markup=confirming_keyboard)
    await state.update_data(trip_mes_id=trip_mes.message_id)
    await FormStates.q9_trip.set()


async def ask_q10(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    if call.data == "yes":
        await state.update_data(trip="Rozi")
    else:
        await state.update_data(trip="Rozi emas")

    async with state.proxy() as data:
        await call.message.edit_text(f"<b>Xizmat safari:</b>\n{data.get('trip')}")
    military_mes = await call.message.answer("<b>Xarbiy xizmatga borganmisiz?</b>", reply_markup=confirming_keyboard)
    await state.update_data(military_mes_id=military_mes.message_id)
    await FormStates.q10_military.set()


async def ask_q10_message(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        await message.bot.delete_message(chat_id, data.get("criminal_mes_id"))
    await message.delete()
    military_mes = await message.answer("<b>Xarbiy xizmatga borganmisiz?</b>", reply_markup=confirming_keyboard)
    await state.update_data(military_mes_id=military_mes.message_id)
    await FormStates.q10_military.set()


async def ask_q11(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    if call.data == "yes":
        await state.update_data(military="Borgan")
    else:
        await state.update_data(military="Bormagan")

    async with state.proxy() as data:
        await call.message.edit_text(f"<b>Xarbiy xizmat:</b>\n{data.get('military')}")
    criminal_mes = await call.message.answer("<b>Sudlanganmisiz?</b>", reply_markup=confirming_keyboard)
    await state.update_data(criminal_mes_id=criminal_mes.message_id)
    await FormStates.q11_criminal.set()


async def ask_q11_message(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        await message.bot.delete_message(chat_id, data.get("license_mes_id"))
    await message.delete()
    criminal_mes = await message.answer("<b>Sudlanganmisiz?</b>", reply_markup=confirming_keyboard)
    await state.update_data(criminal_mes_id=criminal_mes.message_id)
    await FormStates.q11_criminal.set()


async def ask_q12(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    if call.data == "yes":
        await state.update_data(criminal="Xa")
    else:
        await state.update_data(criminal="Yo'q")

    async with state.proxy() as data:
        await call.message.edit_text(f"<b>Sudlanganmi:</b>\n{data.get('criminal')}")
    license_mes = await call.message.answer("<b>Haydovchilik guvohnomasi:</b>", reply_markup=license_keyboard)
    await state.update_data(license_mes_id=license_mes.message_id)
    await FormStates.q12_driver_license.set()


async def ask_q12_message(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        await message.bot.delete_message(chat_id, data.get("car_mes_id"))
    await message.delete()
    license_mes = await message.answer("<b>Haydovchilik guvohnomasi:</b>", reply_markup=license_keyboard)
    await state.update_data(license_mes_id=license_mes.message_id)
    await FormStates.q12_driver_license.set()


async def ask_q13(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    if call.data == "b":
        await state.update_data(driver_license="B")
    elif call.data == "bc":
        await state.update_data(driver_license="BC")
    elif call.data == "other":
        await state.update_data(driver_license="Boshqa")
    else:
        await state.update_data(driver_license="Yo'q")

    async with state.proxy() as data:
        await call.message.edit_text(f"<b>Haydovchilik guvohnomasi:</b>\n{data.get('driver_license')}")
    car_mes = await call.message.answer("<b>O'zingizni shaxsiy avtomobilingiz bormi?</b>",
                                        reply_markup=confirming_keyboard)
    await state.update_data(car_mes_id=car_mes.message_id)
    await FormStates.q13_car.set()


async def ask_q13_message(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        await message.bot.delete_message(chat_id, data.get("ru_lang_mes_id"))
    await message.delete()
    car_mes = await message.answer("<b>O'zingizni shaxsiy avtomobilingiz bormi?</b>", reply_markup=confirming_keyboard)
    await state.update_data(car_mes_id=car_mes.message_id)
    await FormStates.q13_car.set()


async def ask_q14(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    if call.data == "yes":
        await state.update_data(car="Bor")
    else:
        await state.update_data(car="Yo'q")

    async with state.proxy() as data:
        await call.message.edit_text(f"<b>Shaxsiy avtomobil:</b>\n{data.get('car')}")
    ru_lang_mes = await call.message.answer("<b>Rus tilida suxbatlashish darajasi:</b>", reply_markup=level_keyboard)
    await state.update_data(ru_lang_mes_id=ru_lang_mes.message_id)
    await FormStates.q14_ru_lang.set()


async def ask_q14_message(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        await message.bot.delete_message(chat_id, data.get("eng_lang_mes_id"))
    await message.delete()
    ru_lang_mes = await message.answer("<b>Rus tilida suxbatlashish darajasi:</b>", reply_markup=level_keyboard)
    await state.update_data(ru_lang_mes_id=ru_lang_mes.message_id)
    await FormStates.q14_ru_lang.set()


async def ask_q15(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await state.update_data(ru_lang=call.data)
    async with state.proxy() as data:
        await call.message.edit_text(f"<b>Rus tili:</b>\n{data.get('ru_lang')}%")
    eng_lang_mes = await call.message.answer("<b>Ingliz tilida suxbatlashish darajasi:</b>",
                                             reply_markup=level_keyboard)
    await state.update_data(eng_lang_mes_id=eng_lang_mes.message_id)
    await FormStates.q15_eng_lang.set()


async def ask_q15_message(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        await message.bot.delete_message(chat_id, data.get("chi_lang_mes_id"))
    await message.delete()
    eng_lang_mes = await message.answer("<b>Ingiliz tilida suxbatlashish darajasi:</b>", reply_markup=level_keyboard)
    await state.update_data(eng_lang_mes_id=eng_lang_mes.message_id)
    await FormStates.q15_eng_lang.set()


async def ask_q16(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await state.update_data(eng_lang=call.data)
    async with state.proxy() as data:
        await call.message.edit_text(f"<b>Ingiliz tili:</b>\n{data.get('eng_lang')}%")
    chi_lang_mes = await call.message.answer("<b>Xitoy tilida suxbatlashish darajasi:</b>", reply_markup=level_keyboard)
    await state.update_data(chi_lang_mes_id=chi_lang_mes.message_id)
    await FormStates.q16_chi_lang.set()


async def ask_q16_message(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        await message.bot.delete_message(chat_id, data.get("other_lang_mes_id"))
    await message.delete()
    chi_lang_mes = await message.answer("<b>Xitoy tilida suxbatlashish darajasi:</b>", reply_markup=level_keyboard)
    await state.update_data(chi_lang_mes_id=chi_lang_mes.message_id)
    await FormStates.q16_chi_lang.set()


async def ask_q17(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await state.update_data(chi_lang=call.data)
    async with state.proxy() as data:
        await call.message.edit_text(f"<b>Xitoy tili:</b>\n{data.get('chi_lang')}%")
    other_lang_mes = await call.message.answer("<b>Boshqa qanday tilni bilasiz?</b>\n(Turk 75%)")
    await state.update_data(other_lang_mes_id=other_lang_mes.message_id)
    await FormStates.q17_other_lang.set()


async def ask_q17_message(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        try:
            await message.bot.delete_message(chat_id, data.get('word_mes_id'))
        except MessageIdentifierNotSpecified:
            pass
        except MessageToDeleteNotFound:
            pass
    await message.delete()
    other_lang_mes = await message.answer("<b>Boshqa qanday tilni bilasiz?</b>\n(Turk 75%)")
    await state.update_data(other_lang_mes_id=other_lang_mes.message_id)
    await FormStates.q17_other_lang.set()


async def ask_q18(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    await state.update_data(other_lang=message.text)
    await message.delete()
    async with state.proxy() as data:
        try:
            await message.bot.delete_message(chat_id, data.get("other_lang_mes_id"))
        except MessageToDeleteNotFound:
            pass
        try:
            await message.bot.delete_message(chat_id, data.get("excel_mes_id"))
        except MessageIdentifierNotSpecified:
            await message.answer(f"<b>Boshqa til:</b>\n{data.get('other_lang')}")
        except MessageToDeleteNotFound:
            await message.answer(f"<b>Boshqa til:</b>\n{data.get('other_lang')}")

    word_mes = await message.answer("<b>Word dasturini bilishingiz darajasi:</b>", reply_markup=level_keyboard)
    await state.update_data(word_mes_id=word_mes.message_id)
    await FormStates.q18_word_app.set()


async def ask_q19(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await state.update_data(word_app=call.data)
    async with state.proxy() as data:
        await call.message.edit_text(f"<b>Word dasturi:</b>\n{data.get('word_app')}%")
    excel_mes = await call.message.answer("<b>Ecxel dasturini bilishingiz darajsi:</b>", reply_markup=level_keyboard)
    await state.update_data(excel_mes_id=excel_mes.message_id)
    await FormStates.q19_excel_app.set()


async def ask_q19_message(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        await message.bot.delete_message(chat_id, data.get("onec_mes_id"))
    await message.delete()
    excel_mes = await message.answer("<b>Ecxel dasturini bilishingiz darajsi:</b>", reply_markup=level_keyboard)
    await state.update_data(excel_mes_id=excel_mes.message_id)
    await FormStates.q19_excel_app.set()


async def ask_q20(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await state.update_data(excel_app=call.data)
    async with state.proxy() as data:
        await call.message.edit_text(f"<b>Excel dasturi:</b>\n{data.get('excel_app')}%")
    onec_mes = await call.message.answer("<b>1C dasturini bilishingiz darajsi:</b>", reply_markup=level_keyboard)
    await state.update_data(onec_mes_id=onec_mes.message_id)
    await FormStates.q20_1c_app.set()


async def ask_q20_message(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        await message.bot.delete_message(chat_id, data.get("other_app_mes_id"))
    await message.delete()
    onec_mes = await message.answer("<b>1C dasturini bilishingiz darajsi:</b>", reply_markup=level_keyboard)
    await state.update_data(onec_mes_id=onec_mes.message_id)
    await FormStates.q20_1c_app.set()


async def ask_q21(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await state.update_data(onec_app=call.data)
    async with state.proxy() as data:
        await call.message.edit_text(f"<b>1C dasturi:</b>\n{data.get('onec_app')}%")
    other_app_mes = await call.message.answer("<b>Boshqa qanday dasturlarni bilasiz?</b>\n(Adobe Photoshop 75%)")
    await state.update_data(other_app_mes_id=other_app_mes.message_id)
    await FormStates.q21_other_app.set()


async def ask_q21_message(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        try:
            await message.bot.delete_message(chat_id, data.get(''))
        except MessageIdentifierNotSpecified:
            pass
        except MessageToDeleteNotFound:
            pass
    await message.delete()
    other_app_mes = await message.answer("<b>Boshqa qanday dasturlarni bilasiz?</b>\n(Adobe Photoshop 75%)")
    await state.update_data(other_app_mes_id=other_app_mes.message_id)
    await FormStates.q21_other_app.set()


async def ask_q22(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    message_text = message.text
    if message_text != "\U00002B05 Orqaga":
        await state.update_data(other_app=message.text)
    await message.delete()
    async with state.proxy() as data:
        try:
            await message.bot.delete_message(chat_id, data.get("other_app_mes_id"))
        except MessageToDeleteNotFound:
            pass
        try:
            await message.bot.delete_message(chat_id, data.get("photo_mes_id"))
        except MessageIdentifierNotSpecified:
            await message.answer(f"<b>Boshqa dastur:</b>\n{data.get('other_app')}")
        except MessageToDeleteNotFound:
            await message.answer(f"<b>Boshqa dastur:</b>\n{data.get('other_app')}")

    origin_mes = await message.answer("<b>Korxonamiz haqida qayerdan ma'lumot oldingiz?</b>",
                                      reply_markup=origin_keyboard)
    await state.update_data(origin_mes_id=origin_mes.message_id)
    await FormStates.q22_origin.set()


async def ask_q23(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    origin = "Tanish-Bilish" if call.data == "acquainted" else call.data.capitalize()
    async with state.proxy() as data:
        await call.message.edit_text(f"<b>Bizni qayerdan topdingiz:</b>\n{origin}")
    photo_mes = await call.message.answer("<b>Iltimos, o'zingizni rasmingizni jo'nating.</b>")
    await state.update_data(origin=origin, photo_mes_id=photo_mes.message_id)
    await FormStates.q23_photo.set()


async def ready_form(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    photo_id = message.photo[-1].file_id
    async with state.proxy() as data:
        await message.bot.delete_message(chat_id, data.get("photo_mes_id"))
        form = f"<b>Ism va Familiya:</b> {data.get('full_name')}\n" \
               f"<b>Tug'ulgan sana:</b> {data.get('birthdate')}\n" \
               f"<b>Telefon raqam:</b> {data.get('phonenum')}\n" \
               f"<b>Soha yo'nalishi:</b> {data.get('profession')}\n" \
               f"<b>Yashash manzil:</b> {data.get('address')}\n" \
               f"<b>Millat:</b> {data.get('nation')}\n" \
               f"<b>Ma'lumot:</b> {data.get('edu')}\n" \
               f"<b>Oilaviy ahvol:</b> {data.get('marital_status')}\n" \
               f"<b>Xizmat safari:</b> {data.get('trip')}\n" \
               f"<b>Xarbiy xizmat:</b> {data.get('military')}\n" \
               f"<b>Sudlanganmi:</b> {data.get('criminal')}\n" \
               f"<b>Haydovchilik guvohnoma:</b> {data.get('driver_license')}\n" \
               f"<b>Shaxsiy avtomobil:</b> {data.get('car')}\n" \
               f"<b>Rus tili:</b> {data.get('ru_lang')}%\n" \
               f"<b>Ingiliz tili:</b> {data.get('eng_lang')}%\n" \
               f"<b>Xitoy tili:</b> {data.get('chi_lang')}%\n" \
               f"<b>Boshqa tillar:</b> {data.get('other_lang')}\n" \
               f"<b>Word dasturi:</b> {data.get('word_app')}%\n" \
               f"<b>Excel dasturi:</b> {data.get('excel_app')}%\n" \
               f"<b>1C dasturi:</b> {data.get('onec_app')}%\n" \
               f"<b>Boshqa dasturlar:</b> {data.get('other_app')}\n" \
               f"<b>Biz haqimizda ma'lumot olgan manba:</b> {data.get('origin')}\n"
    await message.answer("<b>Sizning ma'lumotlaringiz:</b>")
    await message.answer(form, reply_markup=sending_keyboard)
    await state.update_data(photo_id=photo_id, form_text=form, username=message.from_user.username)
    await FormStates.ready_form.set()


async def finish_form(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    config: Config = call.bot.get("config")
    group_id = config.tg_bot.group_ids[0]
    async with state.proxy() as data:
        await call.message.answer("<b>Anketangiz muvaffaqiyatli jo'natildi!!!</b>\n"
                                  "24 soat ichida ko'rib chiqib siz bilan aloqaga chiqishadi.\n"
                                  "E'tiboringiz uchun raxmat!", reply_markup=menu_keyboard)
        message = await call.bot.send_photo(chat_id=group_id, photo=data.get("photo_id"))
        form_text = data.get("form_text") + f"<b>Telegramdagi nomi:</b> @{data.get('username')}\n" \
                                            f"<b>Telegram ID:</b> {call.message.from_user.id}"
        await call.bot.send_message(chat_id=group_id, text=form_text, reply_to_message_id=message.message_id)
    await state.finish()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(cancel_form, text_contains="Bekor qilish", state="*")
    dp.register_message_handler(about_us, text_contains="Korxona haqida")
    dp.register_message_handler(ask_q1, text_contains="Ro'yhatdan o'tish")
    dp.register_message_handler(ask_q2, regexp=("^[a-zA-Z']{3,}\s[a-zA-Z']{3,}$"), state=FormStates.q1_name)
    dp.register_message_handler(ask_q1, text_contains="\U00002B05 Orqaga", state=FormStates.q2_birthdate)
    dp.register_message_handler(ask_q3, state=FormStates.q2_birthdate, regexp=(
        "\s?(?:0?[1-9]|[12][0-9]|3[01])[-\.](?:0?[1-9]|1[012])[-\.](?:19[6-9]\d|200[0-9])\.?$"))
    dp.register_message_handler(ask_q2, text_contains="\U00002B05 Orqaga", state=FormStates.q3_phonenum)
    dp.register_message_handler(confirm_q3, regexp=("\+998[0-9]{9}$"), state=FormStates.q3_phonenum)
    dp.register_message_handler(confirm_q3, content_types=types.ContentType.CONTACT,
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
    dp.register_message_handler(ask_q4_message, text_contains="\U00002B05 Orqaga", state=FormStates.q5_address)
    dp.register_message_handler(ask_q6, content_types=types.ContentTypes.TEXT, state=FormStates.q5_address)
    dp.register_message_handler(ask_q5_message, text_contains="\U00002B05 Orqaga", state=FormStates.q6_nation)
    dp.register_callback_query_handler(ask_q7, state=FormStates.q6_nation)
    dp.register_message_handler(ask_q6, text_contains="\U00002B05 Orqaga", state=FormStates.q7_edu)
    dp.register_callback_query_handler(ask_q8, state=FormStates.q7_edu)
    dp.register_message_handler(ask_q7_message, text_contains="\U00002B05 Orqaga", state=FormStates.q8_marital_status)
    dp.register_callback_query_handler(ask_q9, state=FormStates.q8_marital_status)
    dp.register_message_handler(ask_q8_message, text_contains="\U00002B05 Orqaga", state=FormStates.q9_trip)
    dp.register_callback_query_handler(ask_q10, state=FormStates.q9_trip)
    dp.register_message_handler(ask_q9_message, text_contains="\U00002B05 Orqaga", state=FormStates.q10_military)
    dp.register_callback_query_handler(ask_q11, state=FormStates.q10_military)
    dp.register_message_handler(ask_q10_message, text_contains="\U00002B05 Orqaga", state=FormStates.q11_criminal)
    dp.register_callback_query_handler(ask_q12, state=FormStates.q11_criminal)
    dp.register_message_handler(ask_q11_message, text_contains="\U00002B05 Orqaga", state=FormStates.q12_driver_license)
    dp.register_callback_query_handler(ask_q13, state=FormStates.q12_driver_license)
    dp.register_message_handler(ask_q12_message, text_contains="\U00002B05 Orqaga", state=FormStates.q13_car)
    dp.register_callback_query_handler(ask_q14, state=FormStates.q13_car)
    dp.register_message_handler(ask_q13_message, text_contains="\U00002B05 Orqaga", state=FormStates.q14_ru_lang)
    dp.register_callback_query_handler(ask_q15, state=FormStates.q14_ru_lang)
    dp.register_message_handler(ask_q14_message, text_contains="\U00002B05 Orqaga", state=FormStates.q15_eng_lang)
    dp.register_callback_query_handler(ask_q16, state=FormStates.q15_eng_lang)
    dp.register_message_handler(ask_q15_message, text_contains="\U00002B05 Orqaga", state=FormStates.q16_chi_lang)
    dp.register_callback_query_handler(ask_q17, state=FormStates.q16_chi_lang)
    dp.register_message_handler(ask_q16_message, text_contains="\U00002B05 Orqaga", state=FormStates.q17_other_lang)
    dp.register_message_handler(ask_q18, content_types=types.ContentType.TEXT,
                                state=FormStates.q17_other_lang)
    dp.register_message_handler(ask_q17_message, text_contains="\U00002B05 Orqaga", state=FormStates.q18_word_app)
    dp.register_callback_query_handler(ask_q19, state=FormStates.q18_word_app)
    dp.register_message_handler(ask_q18, text_contains="\U00002B05 Orqaga", state=FormStates.q19_excel_app)
    dp.register_callback_query_handler(ask_q20, state=FormStates.q19_excel_app)
    dp.register_message_handler(ask_q19_message, text_contains="\U00002B05 Orqaga", state=FormStates.q20_1c_app)
    dp.register_callback_query_handler(ask_q21, state=FormStates.q20_1c_app)
    dp.register_message_handler(ask_q20_message, text_contains="\U00002B05 Orqaga", state=FormStates.q21_other_app)
    dp.register_message_handler(ask_q22, content_types=types.ContentType.TEXT, state=FormStates.q21_other_app)
    dp.register_message_handler(ask_q21_message, text_contains="\U00002B05 Orqaga", state=FormStates.q22_origin)
    dp.register_callback_query_handler(ask_q23, state=FormStates.q22_origin)
    dp.register_message_handler(ask_q22, text_contains="\U00002B05 Orqaga", state=FormStates.q23_photo)
    dp.register_message_handler(ready_form, content_types=types.ContentType.PHOTO, state=FormStates.q23_photo)
    dp.register_callback_query_handler(cancel_form, text_contains="cancel", state=FormStates.ready_form)
    dp.register_callback_query_handler(finish_form, text_contains="send", state=FormStates.ready_form)
    dp.register_message_handler(incorrect_answer, state=FormStates)
