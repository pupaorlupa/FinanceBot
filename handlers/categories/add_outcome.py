from aiogram import types
from loader import dp
from utils.misc import rate_limit
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from states import CategoryStates
from utils.db_api.commands import list_categories, add_category, add_category_shortcut
from keyboards import back_kb
from aiogram.types.reply_keyboard import ReplyKeyboardRemove


@rate_limit(limit=1)
@dp.message_handler(Command('add_outcome'))
async def command_add_outcome(message: types.Message, ):
    await message.answer('Отправь мне название новой категории: ', reply_markup=back_kb)
    await CategoryStates.adding_outcome.set()

@rate_limit(limit=1)
@dp.message_handler(state=CategoryStates.adding_outcome)
async def adding_outcome(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Отмена операции", reply_markup=ReplyKeyboardRemove())
        await state.finish()
        return
    name = message.text
    categories = map(lambda x: x.name, await list_categories(message.from_user.id))
    if name not in categories:
        cat_id = await add_category(name, message.from_user.id, False)
        await add_category_shortcut(name, cat_id, message.from_user.id)

        await message.answer(f'Категория расходов "{name}" успешно создана.', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Категория с таким название уже существует. Новая не была создана', reply_markup=ReplyKeyboardRemove())
    await state.finish()

