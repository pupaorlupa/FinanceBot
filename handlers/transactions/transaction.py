from aiogram import types
from loader import dp
from utils.misc import rate_limit
from string import punctuation
from utils.db_api.commands import (find_user_account_shortcuts,
                                   find_user_category_shortcuts,
                                   list_accounts,
                                   list_categories,
                                   add_category,
                                   add_trans,
                                   select_category,
                                   update_account,
                                   select_account,
                                   delete_transaction)
from aiogram.dispatcher import FSMContext


@rate_limit(limit=1)
@dp.message_handler()
async def add_transaction(message: types.Message, state: FSMContext):
    # поскольку этот хэндлер ловит все сообщения, проверим является ли это сообщение реплаем и если является, проверим на удаление транзакции
    if message.reply_to_message:
        if message.text == "удали":
            try:
                await delete_transaction(message.reply_to_message.message_id)
                await message.answer("Транзакция удалена.")
            except Exception:
                await message.answer("Транзакция не найдена.")
        return


    text = message.text

    # найдем сумму транзакции
    amount = None
    for word in text.split():
        if len(word) > 1 and word[-1] in punctuation:
            word = word[:-1]
        if word.isdigit():
            amount = int(word)
            break
    if not amount:
        await message.answer('Не найдена сумма транзакции, операция не записана.')
        return

    # найдем id счета
    acc_shortcuts = await find_user_account_shortcuts(message.from_user.id)
    acc_id = None
    for s in acc_shortcuts:
        if s.name in text:
            acc_id = s.account_id
            break
    if not acc_id:
        accs = await list_accounts(message.from_user.id)
        for acc in accs:
            if acc.is_main:
                acc_id = acc.id
                break
    if not acc_id:
        await message.answer('Не найдено подходящего счета, операция не записана.')
        return

    # найдем id категории
    category_shortcuts = await find_user_category_shortcuts(message.from_user.id)
    cat_id = None
    for s in category_shortcuts:
        if s.name in text:
            cat_id = s.category_id
            break
    if not cat_id:
        cats = await list_categories(message.from_user.id)
        undef_id = None
        for cat in cats:
            if cat.name == "Нераспознанное":
                undef_id = cat.id
                break
        if not undef_id:
            undef_id = await add_category("Нераспознанное", message.from_user.id, False)
        cat_id = undef_id

    # запишем транзакцию
    cat = await select_category(cat_id)
    await update_account(acc_id, amount, cat.is_income)
    await add_trans(message.from_user.id, cat.is_income, cat_id, amount, text, acc_id, message.message_id)
    acc = await select_account(acc_id)
    await message.answer(f'Записал в <b>{"Доходы" if cat.is_income else "Расходы"}->{cat.name}. Сумма {amount} {"на" if cat.is_income else "с"} {acc.name}</b>.\n'
                         f'Примечание: {text}')
