from aiogram import types
from loader import dp
from utils.misc import rate_limit
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from states import AccountStates
from utils.db_api.commands import add_account, list_accounts, set_main_account
from keyboards import back_kb
from aiogram.types.reply_keyboard import ReplyKeyboardRemove


@rate_limit(limit=1)
@dp.message_handler(Command('set_main_account'))
async def set_main1(message: types.Message, ):
    await message.answer('Отправь мне название счета, который хочешь установить главным: ', reply_markup=back_kb)
    await AccountStates.setting_main.set()

@rate_limit(limit=1)
@dp.message_handler(state=AccountStates.setting_main)
async def set_main2(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Отмена операции", reply_markup=ReplyKeyboardRemove())
        await state.finish()
        return
    name = message.text
    try:
        await set_main_account(message.from_user.id, name)
        await message.answer(f'Счет "{name}" успешно установлен главным.', reply_markup=ReplyKeyboardRemove())
    except ValueError:
        await message.answer('Не найдено счета с таким названием.\nНикаких действий произведено не было.', reply_markup=ReplyKeyboardRemove())
    await state.finish()

