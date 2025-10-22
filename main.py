from src.generators import filter_by_currency, filter_by_currency_csv_exml
from src.processing import filter_by_state, sort_by_date
from src.read_csv_and_exel import read_transactions_from_csv, read_transactions_from_excel
from src.utils import load_transactions
from src.transaction_processor import process_bank_search
from src.widget import get_date, mask_account_card


def main():
    transactions = []
    while True:
        print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
        print("Выберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")
        is_json = False
        choice = input("Пользователь: ")
        if choice == '1':
            file_path = 'data/operations.json'
            transactions = load_transactions(file_path)
            is_json = True
            break
        elif choice == '2':
            file_path = 'data/transactions.csv'
            transactions = read_transactions_from_csv(file_path)
            break
        elif choice == '3':
            file_path = 'data/transactions_excel.xlsx'
            transactions = read_transactions_from_excel(file_path)
            break
        else:
            print("Неверный ввод.")


    # Фильтрация по статусу
    status_options = ['EXECUTED', 'CANCELED', 'PENDING']
    while True:
        status_filter = input(
            "Введите статус, по которому необходимо выполнить фильтрацию. Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\nПользователь: ").strip().upper()
        if status_filter in status_options:
            filtered_transactions = filter_by_state(data=transactions, state=status_filter.upper())
            print(f"Операции отфильтрованы по статусу \"{status_filter}\"")
            break
        else:
            print(f"Статус операции \"{status_filter}\" недоступен.")



    # Дополнительные уточнения
    while True:
        sort_input = input("Отсортировать операции по дате? Да/Нет\nПользователь: ").strip().lower()
        if sort_input == 'да':
            while True:
                order = input("Сортировать по возрастанию или по убыванию?\nПользователь: ").strip().lower()
                if order == 'по возрастанию':
                    sorted_transaction = sort_by_date(data=filtered_transactions, reverse=False)
                    break
                elif order == 'по убыванию':
                    sorted_transaction = sort_by_date(data=filtered_transactions)
                    break
                else:
                    print('Нет такого варианта ответа.')
            break
        elif sort_input == 'нет':
            sorted_transaction = filtered_transactions
            break
        else:
            print('Нет такого варианта ответа.')

    while True:
        only_rub = input("Выводить только рублевые транзакции? Да/Нет\nПользователь: ").strip().lower()
        if only_rub == 'да':
            if is_json:
                filter_by_currency_transaction = list(filter_by_currency(transactions=sorted_transaction, currency_code='RUB'))
            else:
                filter_by_currency_transaction = list(filter_by_currency_csv_exml(transactions=sorted_transaction, currency_code='RUB'))
            break
        elif only_rub == 'нет':
            filter_by_currency_transaction = sorted_transaction
            break
        else:
            print('Нет такого варианта ответа.')

    while True:
        search_word = input("Отфильтровать список транзакций по определенному слову в описании?"
                            " Да/Нет\nПользователь: ").strip().lower()
        if search_word == 'да':
            word = input("Введите слово для поиска:\nПользователь: ")
            search_transaction = process_bank_search(filter_by_currency_transaction, word)
            break
        elif search_word == 'нет':
            search_transaction = filter_by_currency_transaction
            break
        else:
            print('Нет такого варианта ответа.')


    print("Распечатываю итоговый список транзакций...")
    if not search_transaction:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"Всего банковских операций в выборке: {len(search_transaction)}")
        for transaction in search_transaction:
            print(f"{get_date(transaction.get('date'))} {transaction.get('description')}")
            if 'from' in transaction:
                print(transaction.get('to'))
                print(transaction.get('from'))
                print(f'{mask_account_card(transaction.get('to'))} -> {mask_account_card(transaction.get('from'))}')
            else:
                print(f'{mask_account_card(transaction.get('to'))}')
                if is_json:
                    print(f"Сумма: {transaction['operationAmount']['amount']} {transaction['operationAmount']['currency']['name']}\n")
                else:
                    print(f"Сумма: {transaction['amount']} {transaction['currency_name']}\n")

if __name__ == "__main__":
    main()
