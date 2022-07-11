from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminStates(StatesGroup):
    admin_mode = State()
    forms = State()
    stats = State()
    mailing_start = State()
    mailing_confirm = State()


class FormStates(StatesGroup):
    q1_name = State()
    q2_birthday = State()
    q3_phonenum = State()
    q4_profession = State()
    starting_next_form = State()
    q5_address = State()
    q6_nation = State()
    q7_edu = State()
    q8_marital_status = State()
    q9_trip = State()
    q10_military = State()
    q11_criminal = State()
    q12_driver_license = State()
    q13_car = State()
    q14_ru_lang = State()
    q15_eng_lang = State()
    q16_chi_lang = State()
    q17_other_lang = State()
    q18_word_app = State()
    q19_excel_app = State()
    q20_1c_app = State()
    q21_other_app = State()
    q22_origin = State()
    q23_photo = State()
    ready_form = State()
