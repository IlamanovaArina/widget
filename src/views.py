import json
import logging
import os

from src.utils import (currency_rates, for_each_card, get_price_stock,
                       greetings, top_five_transaction, read_excel, checking_current_date)
from src.utils import filter_by_date

logger = logging.getLogger("utils.log")
file_handler = logging.FileHandler("main.log", "w")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

way = r"C:\Users\minac.DESKTOP-L51PJSH\PycharmProjects\widget\data\operations.xlsx"

data_frame = read_excel(way)


def main(date: str, df_transactions, stocks: list, currency: list):
    """Функция создающая JSON ответ для страницы главная"""
    logger.info("Начало работы главной функции (main)")
    final_list = filter_by_date(date, df_transactions)  #####
    time = checking_current_date()
    greeting = greetings(time)
    cards = for_each_card(final_list)
    top_trans = top_five_transaction(final_list)
    stocks_prices = get_price_stock(stocks)
    currency_r = currency_rates(currency)
    logger.info("Создание JSON ответа")
    result = [{
            "greeting": greeting,
            "cards": cards,
            "top_transactions": top_trans,
            "currency_rates": currency_r,
            "stock_prices": stocks_prices,
        }]
    date_json = json.dumps(
        result,
        indent=4,
        ensure_ascii=False,
    )
    logger.info("Завершение работы главной функции (main)")
    return date_json
