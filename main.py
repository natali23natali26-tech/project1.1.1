import re
from collections import Counter
from typing import List, Dict
import json
import csv
import pandas as pd


# def process_bank_search(data: List[Dict], search: str) -> List[Dict]:
#     """
#     Функция для поиска банковских операций по описанию.
#
#     Args:
#         data (List[Dict]): Список словарей с данными о банковских операциях.
#         search (str): Строка поиска.
#
#     Returns:
#         List[Dict]: Список словарей, у которых в описании есть строка поиска.
#     """
#     pattern = re.compile(re.escape(search), re.IGNORECASE)
#     return [transaction for transaction in data if pattern.search(transaction['description'])]
#
#
# def process_bank_operations(data: List[Dict], categories: List[str]) -> Dict[str, int]:
#     """
#     Функция для подсчета количества банковских операций по категориям.
#
#     Args:
#         data (List[Dict]): Список словарей с данными о банковских операциях.
#         categories (List[str]): Список категорий операций.
#
#     Returns:
#         Dict[str, int]: Словарь с количеством операций в каждой категории.
#     """
#     category_counts = Counter()
#
#     for transaction in data:
#         description = transaction['description']
#         for category in categories:
#             if category.lower() in description.lower():
#                 category_counts[category] += 1
#
#     return dict(category_counts)

#
# def load_transactions_from_json(file_path: str) -> List[Dict]:
#     """Загружает транзакции из JSON файла."""
#     with open(file_path, 'r', encoding='utf-8') as f:
#         return json.load(f)
#
#
# def load_transactions_from_csv(file_path: str) -> List[Dict]:
#     """Загружает транзакции из CSV файла."""
#     with open(file_path, 'r', encoding='utf-8') as f:
#         reader = csv.DictReader(f)
#         return list(reader)
#
#
# def load_transactions_from_xlsx(file_path: str) -> List[Dict]:
#     """Загружает транзакции из XLSX файла."""
#     df = pd.read_excel(file_path)
#     return df.to_dict(orient='records')
#

def main():
    transactions = []
    while True:
        print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
        print("Выберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")

        choice = input("Пользователь: ")
        if choice == '1':
            file_path = input("Введите путь к JSON-файлу: ")
            transactions = load_transactions_from_json(file_path)
            break
        elif choice == '2':
            file_path = input("Введите путь к CSV-файлу: ")
            transactions = load_transactions_from_csv(file_path)
            break
        elif choice == '3':
            file_path = input("Введите путь к XLSX-файлу: ")
            transactions = load_transactions_from_xlsx(file_path)
            break
        else:
            print("Неверный ввод.")


    # Фильтрация по статусу
    status_options = ['EXECUTED', 'CANCELED', 'PENDING']
    status_filter = ""
    while True:
        status_filter = input(
            "Введите статус, по которому необходимо выполнить фильтрацию. Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\nПользователь: ").strip().upper()
        if status_filter in status_options:
            print(f"Операции отфильтрованы по статусу \"{status_filter}\"")
            break
        else:
            print(f"Статус операции \"{status_filter}\" недоступен.")

    filtered_transactions = [t for t in transactions if t['status'].upper() == status_filter]

    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Дополнительные уточнения
    sort_transactions = input("Отсортировать операции по дате? Да/Нет\nПользователь: ").strip().lower() == 'да'
    if sort_transactions:
        order = input("Сортировать по возрастанию или по убыванию?\nПользователь: ").strip().lower()
        reverse = True if order == 'по убыванию' else False
        filtered_transactions.sort(key=lambda x: x['date'], reverse=reverse)

    only_rub = input("Выводить только рублевые транзакции? Да/Нет\nПользователь: ").strip().lower() == 'да'
    if only_rub:
        filtered_transactions = [t for t in filtered_transactions if t['currency'] == 'RUB']

    search_word = input(
        "Отфильтровать список транзакций по определенному слову в описании? Да/Нет\nПользователь: ").strip().lower() == 'да'
    if search_word:
        word = input("Введите слово для поиска:\nПользователь: ")
        filtered_transactions = process_bank_search(filtered_transactions, word)

    print("Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(filtered_transactions)}")

    for transaction in filtered_transactions:
        print(f"{transaction['date']} {transaction['description']}")
        print(f"Счет **{transaction['account'][-4:]}")  # последние 4 цифры счета
        print(f"Сумма: {transaction['amount']} {transaction['currency']}\n")


if __name__ == "__main__":
    main()
