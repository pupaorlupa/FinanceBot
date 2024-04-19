from aiogram import types
from loader import dp
from utils.misc import rate_limit
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from states import CategoryStates
from utils.db_api.commands import add_category_shortcut, list_categories, find_category_shortcuts
from keyboards import back_kb
from aiogram.types.reply_keyboard import ReplyKeyboardRemove


@rate_limit(limit=1)
@dp.message_handler(Command('add_category_synonims'))
async def adding_synonims(message: types.Message):
    await message.answer('Отправь мне название категории, синонимы для которой ты хочешь написать:', reply_markup=back_kb)
    await CategoryStates.adding_synonims1.set()

@rate_limit(limit=1)
@dp.message_handler(state=CategoryStates.adding_synonims1)
async def adding_cat_synonims1(message: types.Message, state: FSMContext):
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
    if not found:
        await message.answer("У вас нет категории с таким названием.", reply_markup=ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.answer("После добавления новых синонимов, старые будут стерты.")
        shortcuts = await find_category_shortcuts(found.id)
        answer = []
        for sh in shortcuts:
            answer.append(sh.name)
        await message.answer("Ваши текущие синонимы:\n" + " ".join(answer))
        await message.answer("<b>Через пробел</b> введите синонимы, которые вы хотите использовать:", reply_markup=back_kb)
        await state.update_data(cat_id=found.id)
        await CategoryStates.adding_synonims2.set()

@rate_limit(limit=1)
@dp.message_handler(state=CategoryStates.adding_synonims2)
async def adding_cat_synonims2(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Отмена операции", reply_markup=ReplyKeyboardRemove())
        await state.finish()
        return
    answer = message.text.split(" ")
    cat_id = (await state.get_data("adding_synonims2"))['cat_id']
    for sh in await find_category_shortcuts(cat_id):
        await sh.delete()
    for syn in answer:
        await add_category_shortcut(syn, cat_id, message.from_user.id)
    await message.answer("Синонимы успешно обновлены.", reply_markup=ReplyKeyboardRemove())
    await state.finish()

