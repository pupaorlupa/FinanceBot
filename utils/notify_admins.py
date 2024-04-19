import logging
from aiogram import Dispatcher
from data.config import admins_id

async def on_startup_notify_admins(dp: Dispatcher):
    for admin in admins_id:
        try:
            text = "PythonFinance_bot запущен"
            await dp.bot.send_message(chat_id=admin, text=text)
        except Exception as err:
            logging.exception(err)
