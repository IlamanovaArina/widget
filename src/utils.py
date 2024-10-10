# Вспомогательные функции, для работы функции страницы «Главная»,
import datetime
import pandas as pd

from src.reports import info_decorator


def checking_current_date():
    """ Функция вормирует время формата:
    YYYY-MM-DD HH:MM:SS"""

    today_date = datetime.datetime.now().today()
    today_time = today_date.strftime("%Y-%m-%d %H:%M:%S")

    return today_time


def date(time: str):  # json
    """Функция для страницы «Главная»
    принимает на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS"""
    time_received = datetime.datetime.strptime(time[-8:], "%H:%M:%S")

    dictionary_time_limit = {"00:00:00": "05:59:59", "06:00:00": "11:59:59", "12:00:00": "17:59:59",
                             "18:00:00": "23:59:59"}

    for key, value in dictionary_time_limit.items():
        from_time = datetime.datetime.strptime(key, "%H:%M:%S")
        to_time = datetime.datetime.strptime(value, "%H:%M:%S")

        if from_time <= time_received <= to_time:
            return "Доброй ночи"
        elif from_time <= time_received <= to_time:
            return "Доброе утра"
        elif from_time <= time_received <= to_time:
            return "Добрый день"
        elif from_time <= time_received <= to_time:
            return "Добрый вечер"


greeting = date(checking_current_date())

print(date(checking_current_date()))


def reading_tables_xlsx(file_xlsx: str) -> list:
    """Чтение Excel файла и вывод как список словарей"""
    try:
        df = pd.read_excel(file_xlsx)

        # logger_excel.info(f"Открыли файл{file_path_xlsx}")

        transaction_excel = df.to_dict(orient="records")

        # logger_excel.debug("Преобразовали данные из Exsel в список словарей")

        return transaction_excel

    except TypeError as t:
        print(f"Ошибка: {t}")
    #     logger_excel.error(f"Ошибка: {t}")
    except FileNotFoundError as t:
        print(f"Ошибка: {t}")
    #     logger_excel.error(f"Ошибка: {t}")
    except Exception as t:
        print(f"Ошибка: {t}")
    #     logger_excel.error(f"Ошибка: {t}")


file = r"C:\Users\minac.DESKTOP-L51PJSH\PycharmProjects\widget\data\operations.xlsx"
list_transactions = reading_tables_xlsx(file)


def card_information(list_map_data: list): # -> dict:
    """Собираю этот страшный словарь,
    хотя бы кусочек, а там посмотрим"""

    scary_list = {
        "greeting": greeting,
        "cards": [],  # yes
        "top_transactions": [],  #
        "currency_rates": [],  #
        "stock_prices": []  #
    }

    cards = []
    top_transactions = []
    currency_rates = []
    stock_prices = []
    expenses = []

    for dikt in list_map_data:
        #
        cards.append(
            {
                "last_digits": dikt.get('Номер карты'),
                "total_spent": dikt.get('Сумма платежа'),
                "cashback": dikt.get('Бонусы (включая кэшбэк)')
            }
        )

    sort_list_transaction = sorted(list_map_data, key=lambda d: d['Сумма платежа'])  #

    counter = 0
    for dikt_sort in sort_list_transaction:
        counter += 1
        if counter <= 5:
            amount = str(dikt_sort.get('Сумма платежа'))
            #
            top_transactions.append(
                {
                    "date": dikt_sort.get('Дата платежа'),
                    "amount": amount[1:],
                    "category": dikt_sort.get('Категория'),
                    "description": dikt_sort.get('Описание')
                }
            )
            # print(dikt_sort['Сумма платежа'])


    scary_list["cards"] = cards  #
    scary_list["top_transactions"] = top_transactions  #
    # scary_list["currency_rates"] =   # Курс валют.

    # scary_list["stock_prices"] =   # Стоимость акций из S&P 500.

    print(f"{cards} \n __________Это другая проверка: cards __________ ")
    print(2, scary_list)


result = [
        {
            'Дата операции': '27.11.2018 22:40:20',
            'Дата платежа': '29.11.2018',
            'Номер карты': '*7197',
            'Статус': 'OK',
            'Сумма операции': -485.0,
            'Валюта операции': 'RUB',
            'Сумма платежа': -485.0,
            'Валюта платежа': 'RUB',
            'Кэшбэк': "nan",
            'Категория': 'Фастфуд',
            'MCC': 5814.0,
            'Описание': 'Теремок',
            'Бонусы (включая кэшбэк)': 9,
            'Округление на инвесткопилку': 0,
            'Сумма операции с округлением': 485.0
        },
        {
            'Дата операции': '27.11.2018 16:06:21',
            'Дата платежа': '29.11.2018',
            'Номер карты': '*7197',
            'Статус': 'OK',
            'Сумма операции': -200.0, 'Валюта операции': 'RUB', 'Сумма платежа': -200.0, 'Валюта платежа': 'RUB',
            'Кэшбэк': "nan",
            'Категория': 'Ж/д билеты', 'MCC': 4111.0, 'Описание': 'Метро Санкт-Петербург',
            'Бонусы (включая кэшбэк)': 4,
            'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 200.0},
        {
            'Дата операции': '27.11.2018 13:41:48', 'Дата платежа': '29.11.2018', 'Номер карты': '*7197',
         'Статус': 'OK',
         'Сумма операции': -215.38, 'Валюта операции': 'RUB', 'Сумма платежа': -215.38, 'Валюта платежа': 'RUB',
         'Кэшбэк': "nan",
         'Категория': 'Супермаркеты', 'MCC': 5499.0, 'Описание': 'Колхоз', 'Бонусы (включая кэшбэк)': 4,
         'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 215.38},
        {
            'Дата операции': '26.11.2018 15:56:29', 'Дата платежа': '28.11.2018', 'Номер карты': '*7197',
         'Статус': 'OK',
         'Сумма операции': -67.29, 'Валюта операции': 'RUB', 'Сумма платежа': -67.29, 'Валюта платежа': 'RUB',
         'Кэшбэк': "nan",
         'Категория': 'Супермаркеты', 'MCC': 5411.0, 'Описание': 'Пятёрочка', 'Бонусы (включая кэшбэк)': 1,
         'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 67.29},
        {'Дата операции': '26.11.2018 15:44:09', 'Дата платежа': '28.11.2018', 'Номер карты': '*7197',
         'Статус': 'OK',
         'Сумма операции': -53.0, 'Валюта операции': 'RUB', 'Сумма платежа': -53.0, 'Валюта платежа': 'RUB',
         'Кэшбэк': "nan",
         'Категория': 'Аптеки', 'MCC': 5912.0, 'Описание': 'Аптека Радуга', 'Бонусы (включая кэшбэк)': 1,
         'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 53.0}]

# print(4, card_information(result))
