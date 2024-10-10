# Вспомогательные функции, для работы функции страницы «Главная»,
import os
import datetime
from typing import Any

import pandas as pd

from utils import setup_logger


current_dir = os.path.dirname(os.path.abspath(__file__))
file_path_1 = os.path.join(current_dir, "../logs", "logs.log")
logger = setup_logger("utils", file_path_1)


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


def card_information(list_map_data: list) -> list[dict]:
    """Собираю этот страшный словарь,
    хотя бы кусочек, а там посмотрим"""
    cards = []

    for transaction in list_map_data:
        card_number = transaction.get("Номер карты")

        if not card_number or str(card_number).strip().lower() == "nan":
            continue
        else:
            #
            cards.append(
                {
                    "last_digits": transaction.get('Номер карты'),
                    "total_spent": transaction.get('Сумма платежа'),
                    "cashback": transaction.get('Бонусы (включая кэшбэк)')
                }
            )
    return cards


def top_transactions_information(list_map_data: list) -> list[dict]:
    top_transactions = []
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

    return top_transactions


# не забыть что функция принимает список ["USD", "EUR"]
def get_exchange_rates(currencies: list[str], api_key_currency: Any, requests=None) -> list[dict]:
    """Функция принимает список кодов валют и возвращает список словарей с валютами и их курсами"""
    exchange_rates = []
    for currency in currencies:

        url = f"https://v6.exchangerate-api.com/v6/{api_key_currency}/latest/{currency}"
        response = requests.get(url)

        logger.info("Выполнен запрос на курс валют")

        if response.status_code == 200:
            data = response.json()

            logger.info(f"Получен ответ от api курса валют: {data}")

            ruble_cost = data["conversion_rates"]["RUB"]
            exchange_rates.append({"currency": currency, "rate": ruble_cost})
        else:
            print(f"Ошибка: {response.status_code}, {response.text}")
            logger.error(f"Ошибка api запроса {response.status_code}, {response.text}")
            exchange_rates.append({"currency": currency, "rate": None})
    logger.info("Курсы валют созданы")
    return exchange_rates


# не забыть что функция принимает список ["AAPL", "AMZN", "GOOGL"]
def get_stocks_cost(companies: list[str], api_key_stocks: Any, requests=None) -> list[dict]:
    """Функция принимает список кодов компаний и возвращает словарь со стоимостью акций каждой переданной компании"""

    stocks_cost = []
    for company in companies:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={company}&apikey={api_key_stocks}"
        response = requests.get(url)
        logger.info("Выполнен запрос на курс акций")

        if response.status_code == 200:
            data = response.json()
            logger.info(f"Получен ответ от api курса акций: {data}")
            time_series = data.get("Time Series (Daily)")

            if time_series:
                latest_date = max(time_series.keys())
                latest_data = time_series[latest_date]
                stock_cost = latest_data["4. close"]
                stocks_cost.append({"stock": company, "price": float(stock_cost)})
            else:
                print(f"Ошибка: данные для компании {company} недоступны. API ответ {data}")
                logger.error(f"Ошибка ответа: {data}")
                stocks_cost.append({"stock": company, "price": None})
        else:
            print(f"Ошибка: {response.status_code}, {response.text}")
            logger.error(f"Ошибка api запроса {response.status_code}, {response.text}")
            stocks_cost.append({"stock": company, "price": None})
    logger.info("Стоимость акций создана")
    return stocks_cost
