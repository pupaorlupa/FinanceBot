from aiogram import types
from loader import dp
from utils.misc import rate_limit
from aiogram.dispatcher.filters import Command
from utils.db_api.commands import list_categories, find_category_shortcuts
from emoji import emojize

@rate_limit(limit=1)
@dp.message_handler(Command('categories'))
async def command_list_categories(message: types.Message):
    categories = await list_categories(message.from_user.id)
    answer = []
    for cat in categories:
        if cat.is_income:
            answer.append(cat.name + emojize(':chart_increasing:'))
            answer.append("Доступные синонимы: " + " ".join(map(lambda x: x.name, await find_category_shortcuts(cat.id))))
    for cat in categories:
        if not cat.is_income:
            answer.append(cat.name + emojize(':chart_decreasing:'))
            answer.append("Доступные синонимы: " + " ".join(map(lambda x: x.name, await find_category_shortcuts(cat.id))))
    if not answer:
        await message.answer('У вас нет активных категорий.')
    else:
        await message.answer("\n".join(answer))

