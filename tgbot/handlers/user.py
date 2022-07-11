import asyncio
from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

from tgbot.config import Config
from tgbot.keyboards.inline import cancel_keyboard, menu_control_keyboard, only_confirming_keyboard, \
    professions_keyboard, fill_form_keyboard, nations_keyboard, edu_keyboard, marital_status_keyboard, \
    confirming_keyboard, license_keyboard, level_keyboard, origin_keyboard, sending_keyboard
from tgbot.keyboards.reply import user_menu, admin_menu
from tgbot.misc.states import FormStates
from tgbot.services.database import DBCommands

db = DBCommands("tgbot\db.db")


async def user_start(message: types.Message, state: FSMContext):
    """  Greet the user  """
    await state.finish()
    await message.answer("Assalamu Alaykum!\n\"Lochin Mould\" korxonasinig anketa to'ldirish botiga xush kelibsiz !!!",
                         reply_markup=user_menu)
    await db.register_user()


async def about_us(message: types.Message):
    """  Send to user information about our company when user taps to 'about us' button  """
    await message.answer("Quyidagi xavola orqali \"Lochin Mould\" korxonasining faoliyati haqida to'liq ma'lumotga "
                         "ega bo'lishingiz mumkin.\n"
                         "@Lochin_MouldBot")


async def ask_q1(message: types.Message, state: FSMContext):
    """  Start form filling and ask user's name  """
    anketa_text_message = await message.answer("Anketa:", reply_markup=types.ReplyKeyboardRemove())
    form_message = await message.answer("<b>Ism va familiyangizni to'liq kiriting.</b>\n(Ahmadjon Ahmedov)",
                                        reply_markup=cancel_keyboard)
    await state.update_data(form_message_id=form_message.message_id,
                            anketa_text_message_id=anketa_text_message.message_id)
    await FormStates.q1_name.set()


async def ask_q2(message: types.Message, state: FSMContext):
    """  Ask the user's birthday  """
    await message.delete()
    full_name = message.text
    form_text = f"<b>Ism va Familiya:</b> {full_name}\n"
    async with state.proxy() as data:
        await message.bot.edit_message_text(text=form_text, chat_id=message.chat.id,
                                            message_id=data.get("form_message_id"))
        question_message = await message.answer("<b>Tug'ulgan sanangizni kiriting.</b>\n(24.03.1998)",
                                                reply_markup=menu_control_keyboard)
        data.update(full_name=full_name, form_text=form_text, question_message_id=question_message.message_id)
    await FormStates.q2_birthday.set()


async def ask_q3(message: types.Message, state: FSMContext):
    """  Ask the user for phone number  """
    await message.delete()
    async with state.proxy() as data:
        text = data.get("form_text") + f"<b>Tug'ulgan sana:</b> {message.text}\n"
        await message.bot.edit_message_text(text=text, chat_id=message.chat.id, message_id=data.get("form_message_id"))
        await message.bot.edit_message_text(
            text="<b>Siz bilan bog'lanishimiz mumkin bo'lgan telefon raqamni kiriting.</b>\n(+998916830071)",
            chat_id=message.chat.id, message_id=data.get("question_message_id"), reply_markup=menu_control_keyboard)
        data.update(birthday=message.text, form_text=text)
    await FormStates.q3_phonenum.set()


async def confirm_q3(message: types.Message, state: FSMContext):
    """  Ask user to confirm that the phone number was correct  """
    await message.delete()
    phonenum = message.text
    async with state.proxy() as data:
        await message.bot.edit_message_text(text=f"<b>Raqamni to'g'ri terdingizmi?</b>\n{phonenum}",
                                            chat_id=message.chat.id, message_id=data.get("question_message_id"),
                                            reply_markup=only_confirming_keyboard)
        data.update(phonenum=phonenum)


async def callback_no(call: types.CallbackQuery):
    """  Ask again user's phone number if previous was incorrect  """
    await call.answer(cache_time=5)  # Simple anti-flood
    await call.message.edit_text(text="<b>Siz bilan bog'lanishimiz mumkin bo'lgan telefon raqamni kiriting.</b>\n"
                                      "(+998916830071)", reply_markup=menu_control_keyboard)


async def ask_q4(call: types.CallbackQuery, state: FSMContext):
    """  Ask user for direction of profession  """
    await call.answer(cache_time=5)  # Simple anti-flood
    async with state.proxy() as data:
        form_text = data.get("form_text") + f"<b>Telefon raqam:</b> {data.get('phonenum')}\n"
        await call.bot.edit_message_text(text=form_text, chat_id=call.message.chat.id,
                                         message_id=data.get("form_message_id"))
    await call.message.edit_text("<b>Sohangiz bo'yicha yo'nalishni tanlang.</b>", reply_markup=professions_keyboard)
    await state.update_data(form_text=form_text)
    await FormStates.q4_profession.set()


async def show_sales_manager(call: types.CallbackQuery, state: FSMContext):
    """  Show the requirements of the chosen profession  """
    await call.answer(cache_time=5)  # Simple anti-flood
    await call.message.delete()
    question_message = await call.message.answer_photo(
        photo="AgACAgIAAxkBAAMpYrhbgtoqxAdBaHdumnLYniJ-bo8AAvu9MRs-rchJDnZ6Hb3Nh3kBAAMCAANzAAMpBA",
        caption="<b>Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.</b>",
        reply_markup=fill_form_keyboard)
    await state.update_data(profession="Savdo menejment bo'limi", question_message_id=question_message.message_id)
    await FormStates.starting_next_form.set()


async def show_advertising(call: types.CallbackQuery, state: FSMContext):
    """  Show the requirements of the chosen profession  """
    await call.answer(cache_time=5)  # Simple anti-flood
    await call.message.delete()
    question_message = await call.message.answer_photo(
        photo="AgACAgIAAxkBAAMrYrhbifFoZ8BCIjFIbIsBSDGMiuwAAvy9MRs-rchJCInBDM2haNwBAAMCAANzAAMpBA",
        caption="<b>Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.</b>",
        reply_markup=fill_form_keyboard)
    await state.update_data(profession="Reklama bo'limi", question_message_id=question_message.message_id)
    await FormStates.starting_next_form.set()


async def show_finance(call: types.CallbackQuery, state: FSMContext):
    """  Show the requirements of the chosen profession  """
    await call.answer(cache_time=5)  # Simple anti-flood
    await call.message.delete()
    question_message = await call.message.answer_photo(
        photo="AgACAgIAAxkBAAMtYrhbjk2ePInGw8xpUkBb0FZIvFwAAv29MRs-rchJimKAScX7v9sBAAMCAANzAAMpBA",
        caption="<b>Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.</b>",
        reply_markup=fill_form_keyboard)
    await state.update_data(profession="Moliya bo'limi", question_message_id=question_message.message_id)
    await FormStates.starting_next_form.set()


async def show_hr(call: types.CallbackQuery, state: FSMContext):
    """  Show the requirements of the chosen profession  """
    await call.answer(cache_time=5)  # Simple anti-flood
    await call.message.delete()
    question_message = await call.message.answer_photo(
        photo="AgACAgIAAxkBAAMvYrhbkAmk9p7HkulrFEdP8ZGZCoEAAv69MRs-rchJjbLDYUIPp5ABAAMCAANzAAMpBA",
        caption="<b>Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.</b>",
        reply_markup=fill_form_keyboard)
    await state.update_data(profession="Kadrlar bo'limi", question_message_id=question_message.message_id)
    await FormStates.starting_next_form.set()


async def show_accounting(call: types.CallbackQuery, state: FSMContext):
    """  Show the requirements of the chosen profession  """
    await call.answer(cache_time=5)  # Simple anti-flood
    await call.message.delete()
    question_message = await call.message.answer_photo(
        photo="AgACAgIAAxkBAAMxYrhblHwWoOTbakxP0SsQIrASJtMAAv-9MRs-rchJlawTFod5eosBAAMCAANzAAMpBA",
        caption="<b>Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.</b>",
        reply_markup=fill_form_keyboard)
    await state.update_data(profession="Buxgalteriya bo'limi", question_message_id=question_message.message_id)
    await FormStates.starting_next_form.set()


async def show_marketing(call: types.CallbackQuery, state: FSMContext):
    """  Show the requirements of the chosen profession  """
    await call.answer(cache_time=5)  # Simple anti-flood
    await call.message.delete()
    question_message = await call.message.answer_photo(
        photo="AgACAgIAAxkBAAMzYrhbl0Q-adt61qhgOUTlrX3dgoEAA74xGz6tyEkwI1jttSW-UwEAAwIAA3MAAykE",
        caption="<b>Siz tanlagan soha hodimlari yuqorida ko'rsatilgan talablarga javob berishi kerak.</b>",
        reply_markup=fill_form_keyboard)
    await state.update_data(profession="Marketing bo'limi", question_message_id=question_message.message_id)
    await FormStates.starting_next_form.set()


async def ask_q5(call: types.CallbackQuery, state: FSMContext):
    """  Ask user's address  """
    await call.answer(cache_time=5)  # Simple anti-flood
    async with state.proxy() as data:
        form_text = data.get("form_text") + f"<b>Soha yo'nalishi:</b> {data.get('profession')}\n"
        await call.bot.edit_message_text(text=form_text, chat_id=call.message.chat.id,
                                         message_id=data.get("form_message_id"))
        await call.message.delete()
        question_message = await call.message.answer("<b>Yashash manzilingiz.</b>\n(Qo'qon shahar, Imom Buxoriy 42)",
                                                     reply_markup=menu_control_keyboard)
        data.update(form_text=form_text, question_message_id=question_message.message_id)
    await FormStates.q5_address.set()


async def ask_q6(message: types.Message, state: FSMContext):
    """  Ask user's nation  """
    await message.delete()
    async with state.proxy() as data:
        form_text = data.get("form_text") + f"<b>Yashash manzil:</b> {message.text}\n"
        await message.bot.edit_message_text(form_text, chat_id=message.chat.id, message_id=data.get("form_message_id"))
        await message.bot.edit_message_text(text="<b>Millatingiz:</b>", chat_id=message.chat.id,
                                            message_id=data.get("question_message_id"), reply_markup=nations_keyboard)
        data.update(form_text=form_text, address=message.text)
    await FormStates.q6_nation.set()


async def ask_q7(call: types.CallbackQuery, state: FSMContext):
    """  Ask user's academic degree  """
    await call.answer(cache_time=5)  # Simple anti-flood
    nation = None
    if call.data == "uz":
        nation = "O'zbek"
    elif call.data == "ru":
        nation = "Rus"
    elif call.data == "other":
        nation = "Boshqa"
    async with state.proxy() as data:
        form_text = data.get("form_text") + f"<b>Millat:</b> {nation}\n"
        await call.bot.edit_message_text(text=form_text, chat_id=call.message.chat.id,
                                         message_id=data.get("form_message_id"))
        await call.message.edit_text("<b>Ma'lumotingiz:</b>", reply_markup=edu_keyboard)
        data.update(form_text=form_text, nation=nation)
    await FormStates.q7_edu.set()


async def ask_q8(call: types.CallbackQuery, state: FSMContext):
    """  Ask user's marital status  """
    await call.answer(cache_time=5)  # Simple anti-flood
    edu = None
    if call.data == "secondary":
        edu = "O'rta"
    elif call.data == "secondary_special":
        edu = "O'rta maxsus"
    elif call.data == "bachalor":
        edu = "Oliy | Bakalavr"
    elif call.data == "master":
        edu = "Oliy | Magistr"
    async with state.proxy() as data:
        form_text = data.get("form_text") + f"<b>Ma'lumot:</b> {edu}\n"
        await call.bot.edit_message_text(text=form_text, chat_id=call.message.chat.id,
                                         message_id=data.get("form_message_id"))
        await call.message.edit_text("<b>Oilaviy ahvolingiz:</b>", reply_markup=marital_status_keyboard)
        data.update(form_text=form_text, edu=edu)
    await FormStates.q8_marital_status.set()


async def ask_q9(call: types.CallbackQuery, state: FSMContext):
    """  Ask user's agreement for going on business trips  """
    await call.answer(cache_time=5)  # Simple anti-flood
    marital_status = None
    if call.data == "married":
        marital_status = "Turmush qurgan"
    elif call.data == "not_married":
        marital_status = "Turmush qurmagan"
    async with state.proxy() as data:
        form_text = data.get("form_text") + f"<b>Oilaviy ahvol:</b> {marital_status}\n"
        await call.bot.edit_message_text(text=form_text, chat_id=call.message.chat.id,
                                         message_id=data.get("form_message_id"))
        await call.message.edit_text("<b>Korxona tomonidan xizmat safariga chiqishga rozimisiz?</b>",
                                     reply_markup=confirming_keyboard)
        data.update(form_text=form_text, marital_status=marital_status)
    await FormStates.q9_trip.set()


async def ask_q10(call: types.CallbackQuery, state: FSMContext):
    """  Ask the user did he go to the military  """
    trip = None
    if call.data == "yes":
        trip = "Rozi"
    elif call.data == "no":
        trip = "Rozi emas"
    async with state.proxy() as data:
        form_text = data.get("form_text") + f"<b>Xizmat safari:</b> {trip}\n"
        await call.bot.edit_message_text(text=form_text, chat_id=call.message.chat.id,
                                         message_id=data.get("form_message_id"))
        await call.message.edit_text("<b>Xarbiy xizmatga borganmisiz?</b>", reply_markup=confirming_keyboard)
        data.update(form_text=form_text, trip=trip)
    await FormStates.q10_military.set()


async def ask_q11(call: types.CallbackQuery, state: FSMContext):
    """  Ask the user is he a convict  """
    await call.answer(cache_time=5)  # Simple anti-flood
    military = None
    if call.data == "yes":
        military = "Borgan"
    elif call.data == "no":
        military = "Bormagan"
    async with state.proxy() as data:
        form_text = data.get("form_text") + f"<b>Xarbiy xizmat:</b> {military}\n"
        await call.bot.edit_message_text(text=form_text, chat_id=call.message.chat.id,
                                         message_id=data.get("form_message_id"))
        await call.message.edit_text("<b>Sudlanganmisiz?</b>", reply_markup=confirming_keyboard)
        data.update(form_text=form_text, military=military)
    await FormStates.q11_criminal.set()


async def ask_q12(call: types.CallbackQuery, state: FSMContext):
    """  Ask the user does he have a driver license  """
    await call.answer(cache_time=5)  # Simple anti-flood
    criminal = None
    if call.data == "yes":
        criminal = "Sudlangan"
    elif call.data == "no":
        criminal = "Sudlanmagan"
    async with state.proxy() as data:
        form_text = data.get("form_text") + f"<b>Sudlanganmi:</b> {criminal}\n"
        await call.bot.edit_message_text(text=form_text, chat_id=call.message.chat.id,
                                         message_id=data.get("form_message_id"))
        await call.message.edit_text("<b>Haydovchilik guvohnomangiz:</b>", reply_markup=license_keyboard)
        data.update(form_text=form_text, criminal=criminal)
    await FormStates.q12_driver_license.set()


async def ask_q13(call: types.CallbackQuery, state: FSMContext):
    """  Ask the user does he have a personal car  """
    await call.answer(cache_time=5)  # Simple anti-flood
    driver_license = None
    if call.data == "b":
        driver_license = "B"
    elif call.data == "bc":
        driver_license = "BC"
    elif call.data == "other":
        driver_license = "Boshqa"
    elif call.data == "no":
        driver_license = "Yo'q"
    async with state.proxy() as data:
        form_text = data.get("form_text") + f"<b>Haydovchilik guvohnomasi:</b> {driver_license}\n"
        await call.bot.edit_message_text(text=form_text, chat_id=call.message.chat.id,
                                         message_id=data.get("form_message_id"))
        await call.message.edit_text("<b>O'zingizni shaxsiy avtomobilingiz bormi?</b>",
                                     reply_markup=confirming_keyboard)
        data.update(form_text=form_text, driver_license=driver_license)
    await FormStates.q13_car.set()


async def ask_q14(call: types.CallbackQuery, state: FSMContext):
    """  Ask the user how well he knows Russian  """
    await call.answer(cache_time=5)  # Simple anti-flood
    car = None
    if call.data == "yes":
        car = "Bor"
    elif call.data == "no":
        car = "Yo'q"
    async with state.proxy() as data:
        form_text = data.get("form_text") + f"<b>Shaxsiy avtomobili:</b> {car}\n"
        await call.bot.edit_message_text(text=form_text, chat_id=call.message.chat.id,
                                         message_id=data.get("form_message_id"))
        await call.message.edit_text("<b>Rus tilida suxbatlashish darajangiz:</b>", reply_markup=level_keyboard)
        data.update(form_text=form_text, car=car)
    await FormStates.q14_ru_lang.set()


async def ask_q15(call: types.CallbackQuery, state: FSMContext):
    """  Ask the user how well he knows English  """
    await call.answer(cache_time=5)  # Simple anti-flood
    async with state.proxy() as data:
        form_text = data.get("form_text") + f"<b>Rus tili:</b> {call.data}%\n"
        await call.bot.edit_message_text(text=form_text, chat_id=call.message.chat.id,
                                         message_id=data.get("form_message_id"))
        await call.message.edit_text("<b>Ingliz tilida suxbatlashish darajangiz:</b>", reply_markup=level_keyboard)
        data.update(form_text=form_text, ru_lang=call.data)
    await FormStates.q15_eng_lang.set()


async def ask_q16(call: types.CallbackQuery, state: FSMContext):
    """  Ask the user how well he knows Chinese  """
    await call.answer(cache_time=5)  # Simple anti-flood
    async with state.proxy() as data:
        form_text = data.get("form_text") + f"<b>Ingiliz tili:</b> {call.data}%\n"
        await call.bot.edit_message_text(text=form_text, chat_id=call.message.chat.id,
                                         message_id=data.get("form_message_id"))
        await call.message.edit_text("<b>Xitoy tilida suxbatlashish darajangiz:</b>", reply_markup=level_keyboard)
        data.update(form_text=form_text, eng_lang=call.data)
    await FormStates.q16_chi_lang.set()


async def ask_q17(call: types.CallbackQuery, state: FSMContext):
    """  Ask the user which other languages he knows  """
    await call.answer(cache_time=5)  # Simple anti-flood
    async with state.proxy() as data:
        form_text = data.get("form_text") + f"<b>Xitoy tili:</b> {call.data}%\n"
        await call.bot.edit_message_text(text=form_text, chat_id=call.message.chat.id,
                                         message_id=data.get("form_message_id"))
        question_message = await call.message.edit_text("<b>Boshqa qanday tillarni bilasiz?</b>\n(Turk 75%)",
                                                        reply_markup=menu_control_keyboard)
        data.update(form_text=form_text, chi_lang=call.data, question_message_id=question_message.message_id)
    await FormStates.q17_other_lang.set()


async def ask_q18(message: types.Message, state: FSMContext):
    """  Ask the user how well he knows application 'word'  """
    await message.delete()
    async with state.proxy() as data:
        form_text = data.get("form_text") + f"<b>Boshqa tillar:</b> {message.text}\n"
        await message.bot.edit_message_text(text=form_text, chat_id=message.chat.id,
                                            message_id=data.get("form_message_id"))
        await message.bot.edit_message_text(text="<b>Word dasturini bilishingiz darajasi:</b>", chat_id=message.chat.id,
                                            message_id=data.get("question_message_id"), reply_markup=level_keyboard)
        data.update(form_text=form_text, other_lang=message.text)
    await FormStates.q18_word_app.set()


async def ask_q19(call: types.CallbackQuery, state: FSMContext):
    """  Ask the user how well he knows application 'excel'  """
    await call.answer(cache_time=5)  # Simple anti-flood
    async with state.proxy() as data:
        form_text = data.get("form_text") + f"<b>Word dasturi:</b> {call.data}%\n"
        await call.message.bot.edit_message_text(text=form_text, chat_id=call.message.chat.id,
                                                 message_id=data.get("form_message_id"))
        await call.message.edit_text("<b>Ecxel dasturini bilishingiz darajasi:</b>", reply_markup=level_keyboard)
        data.update(form_text=form_text, word_app=call.data)
    await FormStates.q19_excel_app.set()


async def ask_q20(call: types.CallbackQuery, state: FSMContext):
    """  Ask the user how well he knows application '1c'  """
    await call.answer(cache_time=5)  # Simple anti-flood
    async with state.proxy() as data:
        form_text = data.get("form_text") + f"<b>Excel dasturi:</b> {call.data}%\n"
        await call.message.bot.edit_message_text(text=form_text, chat_id=call.message.chat.id,
                                                 message_id=data.get("form_message_id"))
        await call.message.edit_text("<b>1C dasturini bilishingiz darajasi:</b>", reply_markup=level_keyboard)
        data.update(form_text=form_text, excel_app=call.data)
    await FormStates.q20_1c_app.set()


async def ask_q21(call: types.CallbackQuery, state: FSMContext):
    """  Ask the user which other applications he knows  """
    await call.answer(cache_time=5)  # Simple anti-flood
    async with state.proxy() as data:
        form_text = data.get("form_text") + f"<b>1C dasturi:</b> {call.data}%\n"
        await call.message.bot.edit_message_text(text=form_text, chat_id=call.message.chat.id,
                                                 message_id=data.get("form_message_id"))
        question_message = await call.message.edit_text(
            text="<b>Boshqa qanday dasturlarni bilasiz?</b>\n(Adobe Photoshop 75%)", reply_markup=menu_control_keyboard)
        data.update(form_text=form_text, onec_app=call.data, question_message_id=question_message.message_id)
    await FormStates.q21_other_app.set()


async def ask_q22(message: types.Message, state: FSMContext):
    """  Ask the user about how he found out about our company  """
    await message.delete()
    async with state.proxy() as data:
        form_text = data.get("form_text") + f"<b>Boshqa dasturlar:</b> {message.text}\n"
        await message.bot.edit_message_text(text=form_text, chat_id=message.chat.id,
                                            message_id=data.get("form_message_id"))
        await message.bot.edit_message_text(text="<b>Korxonamiz haqida qayerdan ma'lumot oldingiz?</b>",
                                            chat_id=message.chat.id, message_id=data.get("question_message_id"),
                                            reply_markup=origin_keyboard)
        data.update(form_text=form_text, other_app=message.text)
    await FormStates.q22_origin.set()


async def ask_q23(call: types.CallbackQuery, state: FSMContext):
    """  Ask the user to send his photo  """
    await call.answer(cache_time=5)  # It's a simple anti-flood
    origin = "Tanish-Bilish" if call.data == "acquainted" else call.data.capitalize()
    async with state.proxy() as data:
        form_text = data.get("form_text") + f"<b>Biz haqimizda ma'lumot olgan manba:</b> {origin}\n"
        await call.bot.edit_message_text(text=form_text, chat_id=call.message.chat.id,
                                         message_id=data.get("form_message_id"))
        question_message = await call.message.edit_text("<b>Iltimos, o'zingizni rasmingizni jo'nating.</b>",
                                                        reply_markup=menu_control_keyboard)
        data.update(form_text=form_text, origin=origin, question_message_id=question_message.message_id)
    await FormStates.q23_photo.set()


async def ready_form(message: types.Message, state: FSMContext):
    """  Send to user finished form  """
    photo_id = message.photo[-1].file_id
    await message.delete()
    async with state.proxy() as data:
        await message.bot.delete_message(message.chat.id, data.get("anketa_text_message_id"))
        await message.bot.delete_message(message.chat.id, data.get("question_message_id"))
        await message.bot.delete_message(message.chat.id, data.get("form_message_id"))
        anketa_text_message = await message.answer("<b>Anketangiz tayyor!</b>")
        form_message = await message.answer_photo(photo=photo_id, caption=data.get("form_text"),
                                                  reply_markup=sending_keyboard)
        data.update(anketa_text_message_id=anketa_text_message.message_id, form_message_id=form_message.message_id,
                    photo_id=photo_id)
    await FormStates.ready_form.set()


async def finish_form(call: types.CallbackQuery, state: FSMContext):
    """  Finish form filing and send the form to admin's group  """
    await call.answer(cache_time=5)  # It's a simple anti-flood
    await call.message.edit_reply_markup()
    config: Config = call.bot.get("config")
    group_id = config.tg_bot.group_ids[0]
    admin_ids = config.tg_bot.admin_ids
    async with state.proxy() as data:
        await call.message.answer("<b>Anketangiz muvaffaqiyatli jo'natildi!!!</b>\n"
                                  "24 soat ichida ko'rib chiqib siz bilan aloqaga chiqamiz.\n"
                                  "E'tiboringiz uchun raxmat!",
                                  reply_markup=admin_menu if call.from_user.id in admin_ids else user_menu)
        # Adding to database
        await db.add_form(data.get("full_name"), data.get("birthday"), data.get("phonenum"), data.get("profession"),
                          data.get("address"), data.get("nation"), data.get("edu"), data.get("marital_status"),
                          data.get("trip"), data.get("military"), data.get("criminal"), data.get("driver_license"),
                          data.get("car"), data.get("ru_lang"), data.get("eng_lang"), data.get("chi_lang"),
                          data.get("other_lang"), data.get("word_app"), data.get("excel_app"), data.get("onec_app"),
                          data.get("other_app"), data.get("origin"), data.get("photo_id"))
        message = await call.bot.send_photo(chat_id=group_id, photo=data.get("photo_id"))
        form_text = data.get("form_text") + f"<b>Telegramdagi nomi:</b> @{call.from_user.username}\n" \
                                            f"<b>Telegram ID:</b> {call.message.from_user.id}"
        await call.bot.send_message(chat_id=group_id, text=form_text, reply_to_message_id=message.message_id)
        await state.finish()


async def incorrect_answer(message: types.Message):
    """  Show alert message when user inputs incorrect answer  """
    await message.delete()
    alert = await message.answer("<b>Noto'g'ri ma'lumot kiritdingiz!</b>\n"
                                 "Iltimos, ma'lumotlarni ko'rsatilgan shakilda kiriting.")
    await asyncio.sleep(5)
    await message.bot.delete_message(chat_id=message.chat.id, message_id=alert.message_id)


async def non_functional_messages(message: types.Message):
    """  Show alert message when user sends any non-functional messages  """
    await message.delete()
    alert = await message.answer("<b>Menyudagi funktsiyalardan foydalaning!</b>\n\n"
                                 "<i>Botning ishlash jarayonida xatolikka duch kelsangiz /start'ni bosish orqali "
                                 "botni qayta ishga tushiring.</i>")
    await asyncio.sleep(20)
    await message.bot.delete_message(chat_id=message.chat.id, message_id=alert.message_id)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(about_us, text_contains="Korxona haqida")
    dp.register_message_handler(ask_q1, text_contains="Ro'yhatdan o'tish")
    dp.register_message_handler(ask_q2, content_types=types.ContentType.TEXT, state=FormStates.q1_name)
    dp.register_message_handler(ask_q3, state=FormStates.q2_birthday, regexp=(
        "\s?(?:0?[1-9]|[12][0-9]|3[01])[-\.](?:0?[1-9]|1[012])[-\.](?:19[6-9]\d|200[0-9])\.?$"))
    dp.register_message_handler(confirm_q3, regexp=("\+998[0-9]{9}$"), state=FormStates.q3_phonenum)
    dp.register_message_handler(confirm_q3, content_types=types.ContentType.CONTACT, state=FormStates.q3_phonenum)
    dp.register_callback_query_handler(callback_no, text_contains="no", state=FormStates.q3_phonenum)
    dp.register_callback_query_handler(ask_q4, text_contains="yes", state=FormStates.q3_phonenum)
    dp.register_callback_query_handler(show_sales_manager, text_contains="sales_manager",
                                       state=FormStates.q4_profession)
    dp.register_callback_query_handler(show_advertising, text_contains="advertising", state=FormStates.q4_profession)
    dp.register_callback_query_handler(show_finance, text_contains="finance", state=FormStates.q4_profession)
    dp.register_callback_query_handler(show_hr, text_contains="hr", state=FormStates.q4_profession)
    dp.register_callback_query_handler(show_accounting, text_contains="accounting", state=FormStates.q4_profession)
    dp.register_callback_query_handler(show_marketing, text_contains="marketing", state=FormStates.q4_profession)
    dp.register_callback_query_handler(ask_q5, text_contains="fill_form", state=FormStates.starting_next_form)
    dp.register_message_handler(ask_q6, content_types=types.ContentType.TEXT, state=FormStates.q5_address)
    dp.register_callback_query_handler(ask_q7, state=FormStates.q6_nation)
    dp.register_callback_query_handler(ask_q8, state=FormStates.q7_edu)
    dp.register_callback_query_handler(ask_q9, state=FormStates.q8_marital_status)
    dp.register_callback_query_handler(ask_q10, state=FormStates.q9_trip)
    dp.register_callback_query_handler(ask_q11, state=FormStates.q10_military)
    dp.register_callback_query_handler(ask_q12, state=FormStates.q11_criminal)
    dp.register_callback_query_handler(ask_q13, state=FormStates.q12_driver_license)
    dp.register_callback_query_handler(ask_q14, state=FormStates.q13_car)
    dp.register_callback_query_handler(ask_q15, state=FormStates.q14_ru_lang)
    dp.register_callback_query_handler(ask_q16, state=FormStates.q15_eng_lang)
    dp.register_callback_query_handler(ask_q17, state=FormStates.q16_chi_lang)
    dp.register_message_handler(ask_q18, state=FormStates.q17_other_lang)
    dp.register_callback_query_handler(ask_q19, state=FormStates.q18_word_app)
    dp.register_callback_query_handler(ask_q20, state=FormStates.q19_excel_app)
    dp.register_callback_query_handler(ask_q21, state=FormStates.q20_1c_app)
    dp.register_message_handler(ask_q22, state=FormStates.q21_other_app)
    dp.register_callback_query_handler(ask_q23, state=FormStates.q22_origin)
    dp.register_message_handler(ready_form, content_types=types.ContentType.PHOTO, state=FormStates.q23_photo)
    dp.register_callback_query_handler(finish_form, text_contains="send", state=FormStates.ready_form)
    dp.register_message_handler(incorrect_answer, state=FormStates, content_types=types.ContentType.ANY)
    dp.register_message_handler(non_functional_messages, state="*", content_types=types.ContentType.ANY)
