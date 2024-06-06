import json
from datetime import datetime

def read_and_process_data(filepath):
    with open('operations.json', 'r', encoding="utf-8") as file:
        data = json.load(file)

    # Фильтрация выполненных операций и сортировка по дате
    executed_operations = [op for op in data if op.get('state') == 'EXECUTED']
    executed_operations.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%dT%H:%M:%S.%f'), reverse=True)

    return executed_operations[:5]

def mask_card_number(card_number):
    first_card_number = ''
    for symbol in card_number:
        if symbol.isalpha():
            continue
        elif symbol.isdigit():
            first_card_number += symbol
        elif symbol.isspace():
            continue
    masked_card_number = first_card_number[:6] + '*' * 6 + first_card_number[-4:]
    return masked_card_number
def mask_account_number(account_number):
    first_account_number = ''
    for symbol in account_number:
        if symbol.isalpha():
            continue
        elif symbol.isdigit():
            first_account_number += symbol
        elif symbol.isspace():
            continue
    masked_account_number = "**" + first_account_number[-4:]
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
    card_name = ""
    for symbol in info:
        if symbol.isalpha():
            card_name += symbol
        elif symbol.isspace():
            card_name += symbol
        else:
            continue
    return card_name

def format_and_print_operations(operations):
    for op in operations:
        # Преобразование даты в нужный формат
        date_str = datetime.strptime(op['date'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')
        print(f"{date_str} {op['description']}")

        if 'from' in op:
            if is_bill(op['from']) and is_bill(op['to']):
                print(f"Счет {mask_account_number(op['from'])} -> Счет {mask_account_number(op['to'])}")
            elif is_bill(op['from']) == False and is_bill(op['to']):
                print(f"{find_card_name(op['from'])}{mask_card_number(op['from'])} -> Счет {mask_account_number(op['to'])}")
            elif is_bill(op['from']) and is_bill(op['to']) == False:
                print(f"Счет {mask_account_number(op['from'])} -> {find_card_name(op['to'])}{mask_card_number(op['to'])}")
            else:
                print(f"{find_card_name(op['from'])}{mask_card_number(op['from'])} -> {find_card_name(op['to'])}{mask_card_number(op['to'])}")
        else:
            print(f"Счет {mask_account_number(op['to'])}")

        # Форматирование суммы операции и валюты
        amount_str = format_currency(op['operationAmount']['amount'], op['operationAmount']['currency']['code'])
        print(amount_str)
        print()  # Пустая строка между операциями




# Пример использования
if __name__ == "__main__":
    operations = read_and_process_data('operations.json')
    format_and_print_operations(operations)