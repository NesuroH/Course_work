import json
from datetime import datetime


def get_data(file_path):
    with open(file_path, encoding='utf-8') as file:
        return json.load(file)


def filter_executed_only(data):
    return [op for op in data if op.get('state') == 'EXECUTED']


def sort_by_date(data):
    return sorted(data, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%S.%f'))[-5:]


def mask_card_number(card_number):
    found_card_number = card_number.split()[-1]
    return found_card_number[:4] + ' ' + found_card_number[4:6] + '** ****' + ' ' + found_card_number[-4:]


def mask_account_number(account_number):
    found_account_number = account_number.split()[-1]
    masked_account_number = "**" + found_account_number[-4:]
    return masked_account_number


def is_bill(info):
    return "Счет" in info


def format_currency(amount, currency_code):
    if currency_code == 'RUB':
        return f"{amount} руб."
    elif currency_code == 'USD':
        return f"${amount}"
    else:
        return f"{amount} {currency_code}"


def find_card_name(info):
    words = info.split()
    return ' '.join(words[:-1]) + ' '
