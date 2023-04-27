from aiogram import types
from loader import dp
from utils.misc import rate_limit
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from states import AccountStates
from utils.db_api.commands import add_account_shortcut, list_accounts, find_account_shortcuts
from keyboards import back_kb
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

@rate_limit(limit=1)
@dp.message_handler(Command('add_account_synonims'))
async def adding_synonims(message: types.Message):
    await message.answer('Отправь мне название счета, синонимы для которого ты хочешь написать:', reply_markup=back_kb)
    await AccountStates.adding_synonims1.set()

@rate_limit(limit=1)
@dp.message_handler(state=AccountStates.adding_synonims1)
async def adding_account1(message: types.Message, state: FSMContext):
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
    if not found:
        await message.answer("У вас нет счета с таким названием.", reply_markup=ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.answer("После добавления новых синонимов, старые будут стерты.")
        shortcuts = await find_account_shortcuts(found.id)
        answer = []
        for sh in shortcuts:
            answer.append(sh.name)
        await message.answer("Ваши текущие синонимы:\n" + " ".join(answer))
        await message.answer("<b>Через пробел</b> введите синонимы, которые вы хотите использовать:", reply_markup=back_kb)
        await state.update_data(acc_id=found.id)
        await AccountStates.adding_synonims2.set()

@rate_limit(limit=1)
@dp.message_handler(state=AccountStates.adding_synonims2)
async def adding_synonims2(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Отмена операции", reply_markup=ReplyKeyboardRemove())
        await state.finish()
        return
    answer = message.text.split(" ")
    acc_id = (await state.get_data("adding_synonims2"))['acc_id']
    for sh in await find_account_shortcuts(acc_id):
        await sh.delete()
    for syn in answer:
        await add_account_shortcut(syn, acc_id, message.from_user.id)
    await message.answer("Синонимы успешно обновлены.", reply_markup=ReplyKeyboardRemove())
    await state.finish()
