# test_main.py

import pytest
from main import mask_card_number, mask_account_number, is_bill, format_currency

# Тесты для функции mask_card_number
def test_mask_card_number():
    assert mask_card_number("1234 5678 9012 3456") == "123456******3456"

# Тесты для функции mask_account_number
def test_mask_account_number():
    assert mask_account_number("40702810123456789001") == "**9001"

# Тесты для функции is_bill
def test_is_bill():
    assert is_bill("Счет 123456789") == True
    assert is_bill("Карта 123456789") == False
    assert is_bill("Счет") == True
    assert is_bill("Кредит") == False

# Тесты для функции format_currency
def test_format_currency():
    assert format_currency(100, 'RUB') == "100 руб."
    assert format_currency(100, 'USD') == "$100"
    assert format_currency(100, 'EUR') == "100 EUR"
    assert format_currency(100.5, 'RUB') == "100.5 руб."