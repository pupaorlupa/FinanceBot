from aiogram import types
from loader import dp
from utils.misc import rate_limit
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from states import AccountStates
from utils.db_api.commands import add_account, list_accounts, add_account_shortcut
from keyboards import back_kb
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

@rate_limit(limit=1)
@dp.message_handler(Command('add_account'))
async def command_add_account(message: types.Message, ):
    await message.answer('Отправь мне название нового счета: ', reply_markup=back_kb)
    await AccountStates.adding_account.set()

@rate_limit(limit=1)
@dp.message_handler(state=AccountStates.adding_account)
async def adding_account(message: types.Message, state: FSMContext):
    name = message.text
    if message.text == "Назад":
        await message.answer("Отмена операции", reply_markup=ReplyKeyboardRemove())
        await state.finish()
        return
    accounts = map(lambda x: x.name, await list_accounts(message.from_user.id))
    if name not in accounts:
        acc_id = await add_account(name, message.from_user.id)
        await add_account_shortcut(name, acc_id, message.from_user.id)
        await message.answer(f'Счет "{name}" успешно создан.', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Счет с таким название уже существует. Новый не был создан', reply_markup=ReplyKeyboardRemove())
    await state.finish()
