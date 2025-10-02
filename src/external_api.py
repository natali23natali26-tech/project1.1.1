import requests
import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional

# Загружаем переменные окружения из файла .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

API_KEY = os.getenv('API_KEY')  # Получаем API_KEY из переменной окружения


def get_exchange_rate(currency: str) -> Optional[float]:
    """
    Получает текущий курс валюты по отношению к рублю из Exchange Rates Data API.

    Отправляет запрос в API для получения актуальных курсов валют с базой RUB.
    Если запрос успешен, возвращает курс для указанной валюты.
    В случае ошибки при выполнении запроса или в полученных данных возвращает None.

    :param currency: Код валюты (например, 'USD', 'EUR').
    :return: Курс валюты по отношению к рублю, или None в случае ошибки.
    """
    if not currency:  # Проверяем, что валюта не пустая
        print("Ошибка: код валюты не может быть пустым.")
        return None

    url = f'https://api.apilayer.com/exchangerates_data/latest?base={currency}&symbols=RUB'

    headers = {
        'apikey': API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f'статус ошибки: {response.status_code} - {response.text}')

        data = response.json()

        if 'rates' in data:
            return data['rates']['RUB']  # Возвращаем курс для указанной валюты
    except requests.exceptions.HTTPError as e:
        print(f"HTTP ошибка: {e}")
        return None
    except Exception as e:
        print(f"Ошибка при получении курса валюты: {e}")
        return None


def convert_transaction_to_rub(transaction: dict) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Если валюта транзакции - USD или EUR, запрашивает курс валюты,
    и возвращает сумму в рублях. Если валюта уже в рублях, просто возвращает сумму.

    :param transaction: Словарь с данными о транзакции,
                       должен содержать ключи 'operationAmount.amount' и 'operationAmount.currency.code'.
    :return: Сумма транзакции в рублях как float.
    """
    try:
        amount = transaction['operationAmount']['amount']

        if 'currency' in transaction['operationAmount']:
            currency = transaction['operationAmount']['currency']['code']
            print(f"Currency code: {currency}")
        else:
            print("Currency code is missing in transaction.")
            return 0.0

    except KeyError as e:
        print(f"Ошибка: отсутствует ключ {e} в транзакции.")
        return 0.0

    if currency == 'RUB':
        return float(amount)  # Если валюта уже рубли, возвращаем сумму

    else:
        rate = get_exchange_rate(currency)
    if rate is not None:
        return float(amount) * rate  # Конвертация в рубли
    else:
        print(f"Не удалось получить курс для валюты: {currency}.")
        return 0.0


if __name__ in '__main__':
    print(get_exchange_rate('USD'))
