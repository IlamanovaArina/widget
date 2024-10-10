# Функция для страницы «Главная»
import json
import os
from typing import Any

from src.utils import (
    checking_current_date,
    date,
    reading_tables_xlsx,
    card_information,
    top_transactions_information,
    get_exchange_rates,
    get_stocks_cost
)

with open("../user_settings.json", "r") as file:
    user_choice = json.load(file)
# load_dotenv()
api_key_currency = os.getenv("API_KEY_CURRENCY")
api_key_stocks = os.getenv("API_KEY_STOCKS")
input_date_str = "20.03.2020"


def main(input_date: Any, user_settings: Any, api_key_currency: Any, api_key_stocks: Any) -> Any:
    """Основная функция для генерации JSON-ответа."""
    greeting = date(checking_current_date())
    path = r"../data/operations.xlsx"
    transactions = reading_tables_xlsx(path)
    filtered_transactions = card_information(transactions)
    top_transactions = top_transactions_information(transactions)
    exchange_rates = get_exchange_rates(user_settings["user_currencies"], api_key_currency)
    stocks_cost = get_stocks_cost(user_settings["user_stocks"], api_key_stocks)

    user_data = {
        "greeting": greeting,
        "cards": filtered_transactions,
        "top_transactions": top_transactions,
        "exchange_rates": exchange_rates,
        "stocks": stocks_cost,
    }
    return json.dumps(user_data, ensure_ascii=False, indent=4)
