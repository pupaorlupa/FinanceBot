# from utils.db_api.schemas.user import User

from utils.db_api.schemas.user import User
from utils.db_api.schemas.category import Category
from utils.db_api.schemas.account import Account
from utils.db_api.schemas.category_shortcut import CategoryShortcut
from utils.db_api.schemas.account_shortcut import AccountShortcut
from utils.db_api.schemas.transactions import Transaction

from asyncpg import UniqueViolationError


async def add_user(user_id: int, link: str = ''):
    try:
        user = User(user_id = user_id, link=link)
        await user.create()
        print("Создан пользователь с id = ", user_id)
    except UniqueViolationError:
        print("Пользователь уже существует, id = ", user_id)
        
async def select_all_users():
    users = await User.query.gino.all()
    return users

# ----------------------------------------------------------------------------------

async def add_category(name: str, user_id: int, is_income: bool):
    # try:
    category = Category(user_id = user_id, name=name, is_income = is_income)
    await category.create()
    return category.id
    # except Exception:
    #     print(f"Ошибка создания категории {name} для {user_id}")

async def add_category_shortcut(name:str, category_id: int, user_id: int):
    shortcut = CategoryShortcut(name=name, category_id=category_id, user_id=user_id)
    await shortcut.create()
    return shortcut.id

async def find_category_shortcuts(category_id: int):
    return await CategoryShortcut.query.where(CategoryShortcut.category_id == category_id).gino.all()

async def list_categories(user_id: int):
    return await Category.query.where(Category.user_id == user_id).gino.all()

async def find_user_category_shortcuts(user_id: int):
    return await CategoryShortcut.query.where(CategoryShortcut.user_id == user_id).gino.all()

async def select_category(category_id: int):
    return await Category.query.where(Category.id == category_id).gino.first()

# ----------------------------------------------------------------------------------

async def add_account(name: str, user_id: int):
    account = Account(user_id = user_id, name=name, balance=0, is_main=False)
    await account.create()
    return account.id

async def list_accounts(user_id: int):
    accounts = await Account.query.where(Account.user_id == user_id).gino.all()
    return accounts 

async def set_main_account(user_id: int, name: str):
    accounts = await Account.query.where(Account.user_id == user_id).gino.all()
    found = None
    for acc in accounts:
        if acc.name == name:
            found = acc
    if not found:
        raise ValueError
    for acc in accounts:
        await acc.update(is_main=False).apply()
    await found.update(is_main=True).apply()

async def add_account_shortcut(name:str, account_id: int, user_id: int):
    shortcut = AccountShortcut(name=name, account_id=account_id, user_id=user_id)
    await shortcut.create()
    return shortcut.id

async def find_account_shortcuts(account_id: int):
    return await AccountShortcut.query.where(AccountShortcut.account_id == account_id).gino.all()

async def find_user_account_shortcuts(user_id: int):
    return await AccountShortcut.query.where(AccountShortcut.user_id == user_id).gino.all()

async def update_account(account_id: int, amount: int, is_income: bool):
    acc = await Account.query.where(Account.id == account_id).gino.first()
    if is_income:
        await acc.update(balance=(acc.balance + amount)).apply()
    else:
        await acc.update(balance=(acc.balance - amount)).apply()

async def select_account(account_id: int):
    return await Account.query.where(Account.id == account_id).gino.first()

# ----------------------------------------------------------------------------------

async def add_trans(user_id: int, is_income: bool, category_id: int,
                          amount: int, description: str, account_id: int, message_id: int):
    transaction = Transaction(user_id=user_id, is_income=is_income, category_id=category_id,
                              amount=amount, description=description, account_id=account_id, message_id=message_id)
    await transaction.create()
    return transaction.id

async def list_transactions(user_id: int):
    return await Transaction.query.where(Transaction.user_id == user_id).gino.all()

async def delete_transaction(message_id: int):
    await (await Transaction.query.where(Transaction.message_id == message_id).gino.first()).delete()

# ----------------------------------------------------------------------------------

async def add_link(user_id: int, link: str):
    user = await User.query.where(User.user_id == user_id).gino.first()
    await user.update(link=link).apply()

async def get_link(user_id: int):
    return (await User.query.where(User.user_id == user_id).gino.first()).link
