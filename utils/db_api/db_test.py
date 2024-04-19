# from data import config
from db_python import POSTGRES_URI
# from utils.db_api.db_python import db
from db_python import db
# from utils.db_api.commands import add_user, select_all_users
from commands import (add_user,
                     select_all_users,
                     add_category,
                     add_category_shortcut,
                     list_categories,
                     add_account, 
                     add_transaction,
                     add_account_shortcut)
import asyncio

async def db_test():
    await db.set_bind(POSTGRES_URI)
    await db.gino.drop_all()
    await db.gino.create_all()

    await add_user(123, 'bobus')
    cat = await add_category(123, 'pizda', True)
    await add_category_shortcut('sosat', cat, 123)
    await add_category_shortcut('sdfj', cat, 123)
    await add_category_shortcut('sdfsd', cat, 123)
    await add_category_shortcut('sdfsgr', cat, 123)
    await add_category_shortcut('therg', cat, 123)
    print(await list_categories(123))

    acc = await add_account('сбер', 123)
    await add_account_shortcut('zhopa', cat, 123)
    await add_transaction(123, True, cat, 100, "сосать сосать жопа", acc, 156)
#     await add_user(123, 'bobus')
#     await add_user(123, 'bobus')

#     users = await select_all_users()
#     print(users)

# loop = asyncio.get_event_loop()
# loop.run_until_complete(db_test())
asyncio.run(db_test())
