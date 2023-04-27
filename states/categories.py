from aiogram.dispatcher.filters.state import StatesGroup, State

class CategoryStates(StatesGroup):
    adding_income = State()
    adding_outcome = State()
    adding_synonims = State()
    deleting_category = State()
    adding_synonims1 = State()
    adding_synonims2 = State()

