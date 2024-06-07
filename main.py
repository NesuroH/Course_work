from src.utils import get_data, filter_executed_only, sort_by_date, mask_card_number, mask_account_number, is_bill, \
    format_currency, find_card_name
import json
from datetime import datetime


def format_and_print_operations(operations):
    for op in operations:
        # Преобразование даты в нужный формат
        date_str = datetime.strptime(op['date'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')
        print(f"{date_str} {op['description']}")

        if 'from' in op:
            if is_bill(op['from']) and is_bill(op['to']):
                print(f"Счет {mask_account_number(op['from'])} -> Счет {mask_account_number(op['to'])}")
            elif is_bill(op['from']) == False and is_bill(op['to']):
                print(
                    f"{find_card_name(op['from'])}{mask_card_number(op['from'])} -> Счет {mask_account_number(op['to'])}")
            elif is_bill(op['from']) and is_bill(op['to']) == False:
                print(
                    f"Счет {mask_account_number(op['from'])} -> {find_card_name(op['to'])}{mask_card_number(op['to'])}")
            else:
                print(
                    f"{find_card_name(op['from'])}{mask_card_number(op['from'])} -> {find_card_name(op['to'])}{mask_card_number(op['to'])}")
        else:
            print(f"Счет {mask_account_number(op['to'])}")

        # Форматирование суммы операции и валюты
        amount_str = format_currency(op['operationAmount']['amount'], op['operationAmount']['currency']['code'])
        print(amount_str)
        print()  # Пустая строка между операциями


# Пример использования
if __name__ == "__main__":
    operations = get_data('operations.json')
    sorted_operations = filter_executed_only(operations)
    date_sorted = sort_by_date(sorted_operations)
    format_and_print_operations(date_sorted)
