import gspread
import secrets

gc = gspread.service_account(filename=secrets.PATH_TO_CREDENTIALS)
sh = gc.open("Первый тестовый документ")
sh.sheet1.update("B1", "сосать")
print(sh.sheet1.get("A1"))
