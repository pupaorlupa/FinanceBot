from aiogram import types
from loader import dp
from utils.misc import rate_limit
from aiogram.dispatcher.filters import Command
from utils.db_api.commands import list_accounts

@rate_limit(limit=1)
@dp.message_handler(Command('balance'))
async def command_add_account(message: types.Message):
    accounts = await list_accounts(message.from_user.id)
    answer = []
    for acc in accounts:
        if acc.is_main:
            answer.append("<b>" + acc.name + "</b>: " + str(acc.balance))
        else:
            answer.append(acc.name + ": " + str(acc.balance))
    if not answer:
        await message.answer('У вас нет активных счетов.')
    else:
        await message.answer("\n".join(answer))
