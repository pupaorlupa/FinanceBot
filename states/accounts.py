from aiogram.dispatcher.filters.state import StatesGroup, State

class AccountStates(StatesGroup):
    adding_account = State()
    setting_main = State()
    adding_synonims = State()
    deleting_account = State()
    adding_synonims1 = State()
    adding_synonims2 = State()
