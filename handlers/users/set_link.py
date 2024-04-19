from aiogram import types
from loader import dp, loop
from data import config

from utils.misc import rate_limit
from utils.db_api.commands import add_link, add_user
from aiogram.dispatcher import FSMContext
from states import LinkStates
from keyboards import back_kb
from aiogram.types.reply_keyboard import ReplyKeyboardRemove


@rate_limit(limit=2)
@dp.message_handler(text='/set_link')
async def command_set_link(message: types.Message):
    await add_user(message.from_user.id)
    await message.answer('1) Перейди по ссылке http://sheets.new\n'
                         '2) Добавь service@dulcet-answer-384516.iam.gserviceaccount.com в качестве пользователя-редактора\n'
                         '3) Пришли мне ссылку на новую созданную таблицу',
                         reply_markup=back_kb)
    await LinkStates.setting_link.set()

@rate_limit(limit=2)
@dp.message_handler(state=LinkStates.setting_link)
async def command_start(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer("Отмена операции", reply_markup=ReplyKeyboardRemove())
        await state.finish()
        return
    await add_link(message.from_user.id, message.text)
    await message.answer("Теперь текст вашего сообщения считается ссылкой на sheets таблицу.", reply_markup=ReplyKeyboardRemove())
    await state.finish()
