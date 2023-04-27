from aiogram import types

async def set_default_commands(dp):
    await dp.bot.set_my_commands([types.BotCommand('start', "Запустить бота"),
                                  types.BotCommand('init_guide', "Краткое руководство"),
                                  types.BotCommand('help', 'Помощь'),
                                  types.BotCommand('add_account', 'Добавить счет'),
                                  types.BotCommand('set_main_account', 'Установить главный счет'),
                                  types.BotCommand('add_account_synonims', 'Добавить синонимы к счету'),
                                  types.BotCommand('balance', 'Посмотреть баланс на счетах'),
                                  types.BotCommand('del_account', 'Удалить счет'),
                                  types.BotCommand('add_outcome', 'Добавить категорию расходов'),
                                  types.BotCommand('add_income', 'Добавить категорию доходов'),
                                  types.BotCommand('add_category_synonims', 'Добавить синонимы категории'),
                                  types.BotCommand('categories', 'Посмотреть категории'),
                                  types.BotCommand('del_category', 'Удалить категорию'),
                                  types.BotCommand('set_link', 'Установить ссылку на таблицу'),
                                  types.BotCommand('stats', 'Показать статистику')])
