from aiogram import Bot, Dispatcher, types
from data import config
from asyncio import get_event_loop
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from utils.db_api.db_python import db


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
loop = get_event_loop()
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)



__all__ = ['bot', 'dp', 'db']
