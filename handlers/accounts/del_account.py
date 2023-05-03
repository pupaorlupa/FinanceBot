from aiogram import types
from loader import dp
from utils.misc import rate_limit
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from states import AccountStates
from utils.db_api.commands import list_accounts, find_account_shortcuts
from keyboards import back_kb
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

@rate_limit(limit=1)
@dp.message_handler(Command('del_account'))
async def command_add_account(message: types.Message, ):
    await message.answer('Отправь мне название счета для удаления: ', reply_markup=back_kb)
    await AccountStates.deleting_account.set()

@rate_limit(limit=1)
@dp.message_handler(state=AccountStates.deleting_account)
async def adding_account(message: types.Message, state: FSMContext):
    name = message.text
    if message.text == "Назад":
        await message.answer("Отмена операции", reply_markup=ReplyKeyboardRemove())
        await state.finish()
        return
    accounts = await list_accounts(message.from_user.id)
    found = None
    for acc in accounts:
        if acc.name == name:
            found = acc
            break
    if not found:
        await message.answer("У вас нет счета с таким названием.", reply_markup=ReplyKeyboardRemove())
    else:
        await found.delete()
        shorts = await find_account_shortcuts(found.id)
        for s in shorts:
            await s.delete()
        await message.answer("Счет был успешно удален.", reply_markup=ReplyKeyboardRemove())
    await state.finish()

