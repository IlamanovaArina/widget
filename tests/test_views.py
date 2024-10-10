import os

from src.utils import read_excel
from src.views import filter_by_date
import pytest

way = r"C:\Users\minac.DESKTOP-L51PJSH\PycharmProjects\widget\data\operations.xlsx"
my_list = read_excel(way)
empty_list = []


def test_filter_by_date():
    """Тестирования функции фильтра от заданной даты"""
    assert filter_by_date("2021.11.01", my_list) == [
        {'Дата платежа': '01.11.2021', 'Статус': 'OK', 'Сумма платежа': -228.0, 'Валюта платежа': 'RUB',
         'Категория': 'Супермаркеты', 'Описание': 'Колхоз', 'Номер карты': '*4556'},
        {'Дата платежа': '01.11.2021', 'Статус': 'OK', 'Сумма платежа': -110.0, 'Валюта платежа': 'RUB',
         'Категория': 'Фастфуд', 'Описание': 'Mouse Tail', 'Номер карты': '*4556'},
        {'Дата платежа': '01.11.2021', 'Статус': 'OK', 'Сумма платежа': -525.0, 'Валюта платежа': 'RUB',
         'Категория': 'Одежда и обувь', 'Описание': 'WILDBERRIES', 'Номер карты': '*4556'}]


def test_filter_by_date_emp_att():
    """Тестирования функции фильтра от заданной даты с пустыми атрибутами"""
    assert filter_by_date("", my_list) == []
    assert filter_by_date("2021.11.01", my_list)
    assert filter_by_date("", empty_list) == []
