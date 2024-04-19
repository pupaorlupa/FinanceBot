from aiogram import types
from loader import dp
from utils.misc import rate_limit
from utils.db_api.commands import add_user


@rate_limit(limit=2)
@dp.message_handler(text='/start')
async def command_start(message: types.Message):
    await message.answer('Привет! Я буду помогать тебе следить за финансами и вести статистику.\n'
                         'Чтобы узнать, как работать со мной, напиши /init_guide. Надеюсь на плодотворное сотрудничество!')
    
