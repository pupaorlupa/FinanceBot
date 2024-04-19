async def on_startup(dp):
    
    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)

    import middlewares
    middlewares.setup(dp)

    from loader import db
    from utils.db_api.db_python import on_startup
    await on_startup(dp)

    # print("Удаление базы данных...")
    # await db.gino.drop_all()

    # print("Создание новых таблиц...")
    # await db.gino.create_all()

    print("Успешно.")

    # from utils.notify_admins import on_startup_notify_admins
    # await on_startup_notify_admins(dp)

async def on_shutdown(dp):
    
    from utils.db_api.db_python import on_shutdown
    await on_shutdown(dp)

if __name__ == "__main__":
      from handlers import dp
      from loader import loop
      from aiogram import executor

      executor.start_polling(dp, loop=loop, on_startup=on_startup, on_shutdown=on_shutdown)
