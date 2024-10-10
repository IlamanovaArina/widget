import datetime
import logging
import os
import pandas as pd
import requests
from dotenv import load_dotenv
import json
import urllib.request

load_dotenv()
API_KEY_CUR = os.getenv("API_KEY_CUR")

SP_500_API_KEY = os.getenv("SP_500_API_KEY")

logger = logging.getLogger("utils.log")
file_handler = logging.FileHandler("utils.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def read_excel(path_file: str) -> list[dict]:
    """Функция читает .xlsx файл и возвращает список словарей"""
    df = pd.read_excel(path_file)
    result = df.apply(
        lambda row: {
            "Дата платежа": row["Дата платежа"],
            "Статус": row["Статус"],
            "Сумма платежа": row["Сумма платежа"],
            "Валюта платежа": row["Валюта платежа"],
            "Категория": row["Категория"],
            "Описание": row["Описание"],
            "Номер карты": row["Номер карты"],
        },
        axis=1,
    ).tolist()
    return result

def checking_current_date():
    """ Функция вормирует время формата:
    YYYY-MM-DD HH:MM:SS"""

    today_date = datetime.datetime.now().today()
    today_time = today_date.strftime("%Y-%m-%d %H:%M:%S")

    return today_time

def greetings(time_str: str):  # json
    """Функция для страницы «Главная»
    принимает на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS"""
    time_received = datetime.datetime.strptime(time_str[-8:], "%H:%M:%S")

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


def for_each_card(my_list: list) -> list:
    """Функция создания информации по каждой карте"""
    logger.info("Начало работы функции (for_each_card)")
    cards = {}
    result = []
    logger.info("Перебор транзакций")
    for i in my_list:
        if i["Номер карты"] == "nan" or type(i["Номер карты"]) is float:
            continue
        elif i["Сумма платежа"] == "nan":
            continue
        else:
            if i["Номер карты"][1:] in cards:
                cards[i["Номер карты"][1:]] += float(str(i["Сумма платежа"])[1:])
            else:
                cards[i["Номер карты"][1:]] = float(str(i["Сумма платежа"])[1:])
    for k, v in cards.items():
        result.append({"last_digits": k, "total_spent": round(v, 2), "cashback": round(v / 100, 2)})
    logger.info("Завершение работы функции (for_each_card)")
    return result


def currency_rates(currency: list) -> list[dict]:
    """Функция запроса курса валют"""
    logger.info("Начало работы функции (currency_rates)")
    api_key = API_KEY_CUR
    result = []
    for i in currency:
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{i}"
        with urllib.request.urlopen(url) as response:
            body_json = response.read()
        body_dict = json.loads(body_json)
        result.append({"currency": i, "rate": round(body_dict["conversion_rates"]["RUB"], 2)})

    logger.info("Создание списка словарей для функции - currency_rates")

    logger.info("Окончание работы функции - currency_rates")
    return result


def top_five_transaction(my_list: list) -> list:
    """Функция для получения топ-5 транзакций по сумме платежа"""
    logger.info("Начало работы функции (top_five_transaction)")
    all_transactions = {}
    result = []
    logger.info("Перебор транзакций в функции (top_five_transaction)")
    for i in my_list:
        if i["Категория"] not in all_transactions and str(i["Сумма платежа"])[0:1] != "-":
            if i["Категория"] != "Пополнения":
                all_transactions[i["Категория"]] = float(str(i["Сумма платежа"])[1:])
        elif (
                i["Категория"] in all_transactions
                and float(str(i["Сумма платежа"])[1:]) > all_transactions[i["Категория"]]
        ):
            all_transactions[i["Категория"]] = float(str(i["Сумма платежа"])[1:])
    for i in my_list:
        for k, v in all_transactions.items():
            if k == i["Категория"] and v == float(str(i["Сумма платежа"])[1:]):
                result.append({"date": i["Дата платежа"], "amount": v, "category": k, "description": i["Описание"]})
    logger.info("Окончание работы функции (top_five_transaction)")

    return result


def get_price_stock(stocks: list) -> list:
    """Функция для получения данных об акциях из списка S&P500"""
    logger.info("Начало работы функции (get_price_stock)")
    api_key = SP_500_API_KEY
    stock_prices = []
    logger.info("Функция обрабатывает данные транзакций.")
    for stock in stocks:
        logger.info("Перебор акций в списке 'stocks' в функции (get_price_stock)")
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey={api_key}"
        response = requests.get(url, timeout=5, allow_redirects=False)
        result = response.json()

        stock_prices.append({"stock": stock, "price": round(float(result["Global Quote"]["05. price"]), 2)})
    logger.info("Функция get_price_stock успешно завершила свою работу")
    return stock_prices

def filter_by_date(date: str, my_list: list) -> list:
    """Функция фильтрующая данные по заданной дате"""
    list_by_date = []
    logger.info("Начало работы функции (filter_by_date)")
    if date == "":
        return list_by_date
    year, month, day = int(date[0:4]), int(date[5:7]), int(date[8:10])
    date_obj = datetime.datetime(year, month, day)
    for i in my_list:
        if i["Дата платежа"] == "nan" or type(i["Дата платежа"]) is float: ######
            continue
        elif (
                date_obj
                >= datetime.datetime.strptime(str(i["Дата платежа"]), "%d.%m.%Y")
                >= date_obj - datetime.timedelta(days=day - 1)
        ):
            list_by_date.append(i)
    logger.info("Конец работы функции (filter_by_date)")
    return list_by_date

