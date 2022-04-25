from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):
    pass


class Form(StatesGroup):
    q1_name = State()
    q2_birthdate = State()
    q3_phonenum = State()
    q4_profession = State()
