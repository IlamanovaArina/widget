# Сервисы
import datetime
import json

from src.utils import list_transactions


def srwis(data: list, year: str, month: str):
    """ Функция возвращает json объект с данными по кешу.
    Категория и кэшбэк """
    nev_data = []
    amount = {}

    for dic in data:
        date_obj = datetime.datetime.strptime(dic['Дата операции'], "%d.%m.%Y %H:%M:%S")
        year_t = str(date_obj.year)
        month_t = str(date_obj.month)

        if year in year_t and month in month_t:
            nev_data.append(dic)

            amount[dic["Категория"]] = dic["Бонусы (включая кэшбэк)"]

    result = json.dumps(amount)

    return result


print(srwis(list_transactions, "2018", "11"))