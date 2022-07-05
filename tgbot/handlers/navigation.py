from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot.config import Config
from tgbot.keyboards.inline import cancel_keyboard, menu_control_keyboard, professions_keyboard, nations_keyboard, \
    edu_keyboard, marital_status_keyboard, confirming_keyboard, license_keyboard, level_keyboard, origin_keyboard
from tgbot.keyboards.reply import admin_menu, user_menu
from tgbot.misc.states import FormStates


async def cancel_form(call: types.CallbackQuery, state: FSMContext):
    """  Cancel form filling and back to home menu  """
    await call.answer(cache_time=30)  # It's a simple anti-flood
    config: Config = call.bot.get("config")
    admin_ids = config.tg_bot.admin_ids
    current_state = await state.get_state()
    if current_state != "FormStates:q1_name" and current_state != "FormStates:ready_form":
        async with state.proxy() as data:
            await call.bot.delete_message(call.message.chat.id, data.get("question_message_id"))

    async with state.proxy() as data:
        await call.bot.delete_message(call.message.chat.id, data.get("form_message_id"))
        await call.bot.delete_message(call.message.chat.id, data.get("anketa_text_message_id"))
    await call.message.answer("Ro'yhatdan o'tish bekor qilindi!",
                              reply_markup=admin_menu if call.from_user.id in admin_ids else user_menu)
    await state.finish()


async def back(call: types.CallbackQuery, state: FSMContext):
    """  Go back to the previous question  """
    await call.answer(cache_time=30)  # It's a simple anti-flood
    current_state = await state.get_state()

    if current_state == "FormStates:q2_birthday":
        async with state.proxy() as data:
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get("form_message_id"))
            form_message = await call.message.edit_text(
                "<b>Ism va familiyangizni to'liq kiriting.</b>\n(Ahmadjon Ahmedov)",
                reply_markup=cancel_keyboard)
            data.update(form_message_id=form_message.message_id)
        await FormStates.q1_name.set()

    elif current_state == "FormStates:q3_phonenum":
        async with state.proxy() as data:
            form_text = data.get("form_text")
            last_question_index = form_text.find("<b>Tug'ulgan sana:</b>")
            form_text = form_text[:last_question_index]  # Form text that deleted the answer to last question
            await call.message.delete()
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get("form_message_id"))
            form_message = await call.message.answer(text=form_text)
            question_message = await call.message.answer(text="<b>Tug'ulgan sanangizni kiriting.</b>\n(24.03.1998)",
                                                         reply_markup=menu_control_keyboard)
            data.update(form_text=form_text, question_message_id=question_message.message_id,
                        form_message_id=form_message.message_id)
        await FormStates.q2_birthday.set()

    elif current_state == "FormStates:q4_profession":
        async with state.proxy() as data:
            form_text = data.get("form_text")
            last_question_index = form_text.find("<b>Telefon raqam:</b>")
            form_text = form_text[:last_question_index]  # Form text that deleted the answer to last question
            await call.message.delete()
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get("form_message_id"))
            form_message = await call.message.answer(text=form_text)
            question_message = await call.message.answer(
                "<b>Siz bilan bog'lanishimiz mumkin bo'lgan telefon raqamni kiriting.</b>\n(+998916830071)",
                reply_markup=menu_control_keyboard)
            data.update(form_text=form_text, question_message_id=question_message.message_id,
                        form_message_id=form_message.message_id)
        await FormStates.q3_phonenum.set()

    elif current_state == "FormStates:starting_next_form":
        await call.message.delete()
        question_message = await call.message.answer("<b>Sohangiz bo'yicha yo'nalishni tanlang.</b>",
                                                     reply_markup=professions_keyboard)
        await state.update_data(question_message_id=question_message.message_id)
        await FormStates.q4_profession.set()

    elif current_state == "FormStates:q5_address":
        async with state.proxy() as data:
            form_text = data.get("form_text")
            last_question_index = form_text.find("<b>Soha yo'nalishi:</b>")
            form_text = form_text[:last_question_index]  # Form text that deleted the answer to last question
            await call.message.delete()
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get("form_message_id"))
            form_message = await call.message.answer(text=form_text)
            question_message = await call.message.answer("<b>Sohangiz bo'yicha yo'nalishni tanlang.</b>",
                                                         reply_markup=professions_keyboard)
            data.update(form_text=form_text, question_message_id=question_message.message_id,
                        form_message_id=form_message.message_id)
        await FormStates.q4_profession.set()

    elif current_state == "FormStates:q6_nation":
        async with state.proxy() as data:
            form_text = data.get("form_text")
            last_question_index = form_text.find("<b>Yashash manzil:</b>")
            form_text = form_text[:last_question_index]  # Form text that deleted the answer to last question
            await call.message.delete()
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get("form_message_id"))
            form_message = await call.message.answer(text=form_text)
            question_message = await call.message.answer(
                "<b>Yashash manzilingiz.</b>\n(Qo'qon shahar, Imom Buxoriy 42)",
                reply_markup=menu_control_keyboard)
            data.update(form_text=form_text, question_message_id=question_message.message_id,
                        form_message_id=form_message.message_id)
        await FormStates.q5_address.set()

    elif current_state == "FormStates:q7_edu":
        async with state.proxy() as data:
            form_text = data.get("form_text")
            last_question_index = form_text.find("<b>Millat:</b>")
            form_text = form_text[:last_question_index]  # Form text that deleted the answer to last question
            await call.message.delete()
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get("form_message_id"))
            form_message = await call.message.answer(text=form_text)
            question_message = await call.message.answer("<b>Millatingiz:</b>", reply_markup=nations_keyboard)
            data.update(form_text=form_text, question_message_id=question_message.message_id,
                        form_message_id=form_message.message_id)
        await FormStates.q6_nation.set()

    elif current_state == "FormStates:q8_marital_status":
        async with state.proxy() as data:
            form_text = data.get("form_text")
            last_question_index = form_text.find("<b>Ma'lumot:</b>")
            form_text = form_text[:last_question_index]  # Form text that deleted the answer to last question
            await call.message.delete()
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get("form_message_id"))
            form_message = await call.message.answer(text=form_text)
            question_message = await call.message.answer("<b>Ma'lumotingiz:</b>", reply_markup=edu_keyboard)
            data.update(form_text=form_text, question_message_id=question_message.message_id,
                        form_message_id=form_message.message_id)
        await FormStates.q7_edu.set()

    elif current_state == "FormStates:q9_trip":
        async with state.proxy() as data:
            form_text = data.get("form_text")
            last_question_index = form_text.find("<b>Oilaviy ahvol</b>")
            form_text = form_text[:last_question_index]  # Form text that deleted the answer to last question
            await call.message.delete()
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get("form_message_id"))
            form_message = await call.message.answer(text=form_text)
            question_message = await call.message.answer("<b>Oilaviy ahvolingiz:</b>",
                                                         reply_markup=marital_status_keyboard)
            data.update(form_text=form_text, question_message_id=question_message.message_id,
                        form_message_id=form_message.message_id)
        await FormStates.q8_marital_status.set()

    elif current_state == "FormStates:q10_military":
        async with state.proxy() as data:
            form_text = data.get("form_text")
            last_question_index = form_text.find("<b>Xizmat safari:</b>")
            form_text = form_text[:last_question_index]  # Form text that deleted the answer to last question
            await call.message.delete()
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get("form_message_id"))
            form_message = await call.message.answer(text=form_text)
            question_message = await call.message.answer(
                "<b>Korxona tomonidan xizmat safariga chiqishga rozimisiz?</b>",
                reply_markup=confirming_keyboard)
            data.update(form_text=form_text, question_message_id=question_message.message_id,
                        form_message_id=form_message.message_id)
        await FormStates.q9_trip.set()

    elif current_state == "FormStates:q11_criminal":
        async with state.proxy() as data:
            form_text = data.get("form_text")
            last_question_index = form_text.find("<b>Xarbiy xizmat:</b>")
            form_text = form_text[:last_question_index]  # Form text that deleted the answer to last question
            await call.message.delete()
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get("form_message_id"))
            form_message = await call.message.answer(text=form_text)
            question_message = await call.message.answer("<b>Xarbiy xizmatga borganmisiz?</b>",
                                                         reply_markup=confirming_keyboard)
            data.update(form_text=form_text, question_message_id=question_message.message_id,
                        form_message_id=form_message.message_id)
        await FormStates.q10_military.set()

    elif current_state == "FormStates:q12_driver_license":
        async with state.proxy() as data:
            form_text = data.get("form_text")
            last_question_index = form_text.find("<b>Sudlanganmi:</b>")
            form_text = form_text[:last_question_index]  # Form text that deleted the answer to last question
            await call.message.delete()
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get("form_message_id"))
            form_message = await call.message.answer(text=form_text)
            question_message = await call.message.answer("<b>Sudlanganmisiz?</b>",
                                                         reply_markup=confirming_keyboard)
            data.update(form_text=form_text, question_message_id=question_message.message_id,
                        form_message_id=form_message.message_id)
        await FormStates.q11_criminal.set()

    elif current_state == "FormStates:q13_car":
        async with state.proxy() as data:
            form_text = data.get("form_text")
            last_question_index = form_text.find("<b>Haydovchilik guvohnomasi:</b>")
            form_text = form_text[:last_question_index]  # Form text that deleted the answer to last question
            await call.message.delete()
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get("form_message_id"))
            form_message = await call.message.answer(text=form_text)
            question_message = await call.message.answer("<b>Haydovchilik guvohnomangiz:</b>",
                                                         reply_markup=license_keyboard)
            data.update(form_text=form_text, question_message_id=question_message.message_id,
                        form_message_id=form_message.message_id)
        await FormStates.q12_driver_license.set()

    elif current_state == "FormStates:q14_ru_lang":
        async with state.proxy() as data:
            form_text = data.get("form_text")
            last_question_index = form_text.find("<b>Shaxsiy avtomobili:</b>")
            form_text = form_text[:last_question_index]  # Form text that deleted the answer to last question
            await call.message.delete()
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get("form_message_id"))
            form_message = await call.message.answer(text=form_text)
            question_message = await call.message.answer("<b>O'zingizni shaxsiy avtomobilingiz bormi?</b>",
                                                         reply_markup=confirming_keyboard)
            data.update(form_text=form_text, question_message_id=question_message.message_id,
                        form_message_id=form_message.message_id)
        await FormStates.q13_car.set()

    elif current_state == "FormStates:q15_eng_lang":
        async with state.proxy() as data:
            form_text = data.get("form_text")
            last_question_index = form_text.find("<b>Rus tili:</b>")
            form_text = form_text[:last_question_index]  # Form text that deleted the answer to last question
            await call.message.delete()
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get("form_message_id"))
            form_message = await call.message.answer(text=form_text)
            question_message = await call.message.answer("<b>Rus tilida suxbatlashish darajangiz:</b>",
                                                         reply_markup=level_keyboard)
            data.update(form_text=form_text, question_message_id=question_message.message_id,
                        form_message_id=form_message.message_id)
        await FormStates.q14_ru_lang.set()

    elif current_state == "FormStates:q16_chi_lang":
        async with state.proxy() as data:
            form_text = data.get("form_text")
            last_question_index = form_text.find("<b>Ingiliz tili:</b>")
            form_text = form_text[:last_question_index]  # Form text that deleted the answer to last question
            await call.message.delete()
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get("form_message_id"))
            form_message = await call.message.answer(text=form_text)
            question_message = await call.message.answer("<b>Ingliz tilida suxbatlashish darajangiz:</b>",
                                                         reply_markup=level_keyboard)
            data.update(form_text=form_text, question_message_id=question_message.message_id,
                        form_message_id=form_message.message_id)
        await FormStates.q15_eng_lang.set()

    elif current_state == "FormStates:q17_other_lang":
        async with state.proxy() as data:
            form_text = data.get("form_text")
            last_question_index = form_text.find("<b>Xitoy tili:</b>")
            form_text = form_text[:last_question_index]  # Form text that deleted the answer to last question
            await call.message.delete()
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get("form_message_id"))
            form_message = await call.message.answer(text=form_text)
            question_message = await call.message.answer("<b>Xitoy tilida suxbatlashish darajangiz:</b>",
                                                         reply_markup=level_keyboard)
            data.update(form_text=form_text, question_message_id=question_message.message_id,
                        form_message_id=form_message.message_id)
        await FormStates.q16_chi_lang.set()

    elif current_state == "FormStates:q18_word_app":
        async with state.proxy() as data:
            form_text = data.get("form_text")
            last_question_index = form_text.find("<b>Boshqa tillar:</b>")
            form_text = form_text[:last_question_index]  # Form text that deleted the answer to last question
            await call.message.delete()
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get("form_message_id"))
            form_message = await call.message.answer(text=form_text)
            question_message = await call.message.answer("<b>Boshqa qanday tillarni bilasiz?</b>\n(Turk 75%)",
                                                         reply_markup=menu_control_keyboard)
            data.update(form_text=form_text, question_message_id=question_message.message_id,
                        form_message_id=form_message.message_id)
        await FormStates.q17_other_lang.set()

    elif current_state == "FormStates:q19_excel_app":
        async with state.proxy() as data:
            form_text = data.get("form_text")
            last_question_index = form_text.find("<b>Word dasturi:</b>")
            form_text = form_text[:last_question_index]  # Form text that deleted the answer to last question
            await call.message.delete()
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get("form_message_id"))
            form_message = await call.message.answer(text=form_text)
            question_message = await call.message.answer("<b>Word dasturini bilishingiz darajasi:</b>",
                                                         reply_markup=level_keyboard)
            data.update(form_text=form_text, question_message_id=question_message.message_id,
                        form_message_id=form_message.message_id)
        await FormStates.q18_word_app.set()

    elif current_state == "FormStates:q20_1c_app":
        async with state.proxy() as data:
            form_text = data.get("form_text")
            last_question_index = form_text.find("<b>Excel dasturi:</b>")
            form_text = form_text[:last_question_index]  # Form text that deleted the answer to last question
            await call.message.delete()
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get("form_message_id"))
            form_message = await call.message.answer(text=form_text)
            question_message = await call.message.answer("<b>Ecxel dasturini bilishingiz darajasi:</b>",
                                                         reply_markup=level_keyboard)
            data.update(form_text=form_text, question_message_id=question_message.message_id,
                        form_message_id=form_message.message_id)
        await FormStates.q19_excel_app.set()

    elif current_state == "FormStates:q21_other_app":
        async with state.proxy() as data:
            form_text = data.get("form_text")
            last_question_index = form_text.find("<b>1C dasturi:</b>")
            form_text = form_text[:last_question_index]  # Form text that deleted the answer to last question
            await call.message.delete()
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get("form_message_id"))
            form_message = await call.message.answer(text=form_text)
            question_message = await call.message.answer("<b>1C dasturini bilishingiz darajasi:</b>",
                                                         reply_markup=level_keyboard)
            data.update(form_text=form_text, question_message_id=question_message.message_id,
                        form_message_id=form_message.message_id)
        await FormStates.q20_1c_app.set()

    elif current_state == "FormStates:q22_origin":
        async with state.proxy() as data:
            form_text = data.get("form_text")
            last_question_index = form_text.find("<b>Boshqa dasturlar:</b>")
            form_text = form_text[:last_question_index]  # Form text that deleted the answer to last question
            await call.message.delete()
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get("form_message_id"))
            form_message = await call.message.answer(text=form_text)
            question_message = await call.message.answer(
                "<b>Boshqa qanday dasturlarni bilasiz?</b>\n(Adobe Photoshop 75%)", reply_markup=menu_control_keyboard)
            data.update(form_text=form_text, question_message_id=question_message.message_id,
                        form_message_id=form_message.message_id)
        await FormStates.q21_other_app.set()

    elif current_state == "FormStates:q23_photo":
        async with state.proxy() as data:
            form_text = data.get("form_text")
            last_question_index = form_text.find("<b>Biz haqimizda ma'lumot olgan manba:</b>")
            form_text = form_text[:last_question_index]  # Form text that deleted the answer to last question
            await call.message.delete()
            await call.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get("form_message_id"))
            form_message = await call.message.answer(text=form_text)
            question_message = await call.message.answer("<b>Korxonamiz haqida qayerdan ma'lumot oldingiz?</b>",
                                                         reply_markup=origin_keyboard)
            data.update(form_text=form_text, question_message_id=question_message.message_id,
                        form_message_id=form_message.message_id)
        await FormStates.q22_origin.set()


def register_navigation(dp: Dispatcher):
    dp.register_callback_query_handler(cancel_form, text_contains="home", state=FormStates)
    dp.register_callback_query_handler(back, text_contains="back", state=FormStates)
