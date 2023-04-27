from aiogram import types
from loader import dp
from utils.misc import rate_limit
from utils.db_api.commands import (add_user,
                                   get_link,
                                   list_transactions,
                                   select_category,
                                   select_account)
from data.config import PATH_TO_CREDENTIALS
import gspread
from gspread.cell import rowcol_to_a1


@rate_limit(limit=2)
@dp.message_handler(text='/stats')
async def command_start(message: types.Message):
    await add_user(message.from_user.id)
    link = await get_link(message.from_user.id)
    gc = gspread.service_account(filename=PATH_TO_CREDENTIALS)
    try:
        sh = gc.open_by_url(link)
        transactions = await list_transactions(message.from_user.id)
        if len(transactions) == 0:
            await message.answer("У вас нет ни одной доступной транзакции.")
            return
        worksheets = sh.worksheets()
        worksheet = None
        for w in worksheets:
            if w.title == "Транзакции":
                worksheet = w
                worksheet.resize(len(transactions) + 1, 6)
                break
        if not worksheet:
            worksheet = sh.add_worksheet(title='Транзакции', rows=len(transactions)+1, cols=6)
        worksheet.clear()
        worksheet.update('A1:F1', [["Категория", "Тип", "Счет", "Сумма", "Описание", "Дата создания"]])
        worksheet.format('A1:F1', {'textFormat': {'bold': True}})
        data = []
        for t in transactions:
            cat = (await select_category(t.category_id)).name
            acc= (await select_account(t.account_id)).name
            data.append([cat, ("Доход" if t.is_income else "Расход"), acc, str(t.amount), t.description, str(t.date_created)[:19]])
        data.sort(key=(lambda x: x[1]))
        worksheet.update(f'A2:{rowcol_to_a1(len(transactions) + 1, 6)}', data)
        worksheet.columns_auto_resize(1, 6)
        await message.answer('Данные в таблице обновлены.')
    except Exception as ex:
        await message.answer("Кажется что-то пошло не так. Возможно, вы указали недействительную ссылку или не выдали права редактора пользователю service@dulcet-answer-384516.iam.gserviceaccount.com")
        raise ex
    

