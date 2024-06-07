# test_main.py
import json
from datetime import datetime
import pytest
from src.utils import get_data, filter_executed_only, sort_by_date, mask_card_number, mask_account_number, is_bill, \
    format_currency, find_card_name

# Sample data for testing
sample_data = [
    {"state": "EXECUTED", "date": "2023-01-01T12:00:00.000", "info": "Payment from card 1234567812345678",
     "amount": 100, "currency_code": "RUB"},
    {"state": "PENDING", "date": "2023-01-02T13:00:00.000", "info": "Payment from card 1234567812345678",
     "amount": 200, "currency_code": "USD"},
    {"state": "EXECUTED", "date": "2023-01-03T14:00:00.000", "info": "Payment from card 1234567812345678",
     "amount": 300, "currency_code": "EUR"},
    # Add more entries as needed for thorough testing
]


def test_get_data(mocker):
    # Mock opening a file and returning sample JSON data
    mocker.patch('builtins.open', mocker.mock_open(read_data=json.dumps(sample_data)))
    assert get_data('fake_path.json') == sample_data


def test_filter_executed_only():
    executed_operations = filter_executed_only(sample_data)
    assert all(op['state'] == 'EXECUTED' for op in executed_operations)


def test_sort_by_date():
    sorted_operations = sort_by_date(sample_data)
    assert sorted_operations == sorted(sample_data, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%S.%f'))[
                                -5:]


def test_mask_card_number():
    assert mask_card_number("Payment from card 1234567812345678") == "1234 56** **** 5678"


def test_mask_account_number():
    assert mask_account_number("Account number 12345678") == "**5678"


def test_is_bill():
    assert is_bill("Счет на оплату услуг") == True
    assert is_bill("Payment from card") == False


def test_format_currency():
    assert format_currency(100, 'RUB') == "100 руб."
    assert format_currency(100, 'USD') == "$100"
    assert format_currency(100, 'EUR') == "100 EUR"


def test_find_card_name():
    assert find_card_name("Payment from card 1234567812345678") == "Payment from card "


# Run the tests
if __name__ == "__main__":
    pytest.main()
