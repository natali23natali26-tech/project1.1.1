import requests

API_KEY = 'P9scVvXKu3F1SdIqsS0nKYndV8xBvxbC'


def get_exchange_rate(currency):
    """
    Получает текущий курс валюты по отношению к рублю из Exchange Rates Data API.

    :param currency: Код валюты (например, 'USD' или 'EUR')
    :return: Курс валюты по отношению к рублю, или None в случае ошибки
    """
    url = f'https://api.apilayer.com/exchangerates_data/latest?base=RUB&symbols={currency}'

    headers = {
        'apikey': API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Вызывает исключение для кода ответа >= 400
        data = response.json()
        return data['rates'].get(currency)  # Возвращаем курс для указанной валюты
    except Exception as e:
        print(f"Ошибка при получении курса валюты: {e}")
        return None


from utils import convert_to_rub
import json
import os


def load_transactions(file_path):
    # Это функция для загрузки данных из JSON-файла,
    # можете использовать ее из utils.py
    if not os.path.exists(file_path):
        print(f"Файл не найден: {file_path}")
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                print("Данные в файле не представляют собой список.")
                return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


if __name__ == "__main__":
    transactions = load_transactions('data/operations.json')
    for transaction in transactions:
        rub_amount = convert_to_rub(transaction)
        print(f"Сумма транзакции в рублях: {rub_amount}")
