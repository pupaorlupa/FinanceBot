from aiogram import types
from loader import dp
from utils.misc import rate_limit
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from states import CategoryStates
from utils.db_api.commands import list_categories, find_category_shortcuts
from keyboards import back_kb

from aiogram.types.reply_keyboard import ReplyKeyboardRemove

@rate_limit(limit=1)
@dp.message_handler(Command('del_category'))
async def command_del_category(message: types.Message):
    await message.answer('Отправь мне название категории для удаления: ', reply_markup=back_kb)
    await CategoryStates.deleting_category.set()

@rate_limit(limit=1)
@dp.message_handler(state=CategoryStates.deleting_category)
async def deleting_category(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Отмена операции", reply_markup=ReplyKeyboardRemove())
        await state.finish()
        return
    name = message.text
    categories = await list_categories(message.from_user.id)
    found = None
    for cat in categories:
        if cat.name == name:
            found = cat
            break
    if not found:
        await message.answer("У вас нет категории с таким названием.", reply_markup=ReplyKeyboardRemove())
    else:
        shorts = await find_category_shortcuts(found.id)
        for s in shorts:
            await s.delete()
        await found.delete()
        await message.answer("Категория была успешно удалена.", reply_markup=ReplyKeyboardRemove())
    await state.finish()


