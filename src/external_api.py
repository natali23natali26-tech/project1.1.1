import requests
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

API_KEY = os.getenv('API_KEY')  # Получаем API_KEY из переменной окружения


def get_exchange_rate(currency):
    """
    Получает текущий курс валюты по отношению к рублю из Exchange Rates Data API.

    Отправляет запрос в API для получения актуальных курсов валют с базой RUB.
    Если запрос успешен, возвращает курс для указанной валюты.
    В случае ошибки при выполнении запроса или в полученных данных возвращает None.

    :param currency: Код валюты (например, 'USD', 'EUR').
    :return: Курс валюты по отношению к рублю, или None в случае ошибки.
    """
    url = f'https://api.apilayer.com/exchangerates_data/latest?base=RUB&symbols={currency}'

    headers = {
        'apikey': API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['rates'].get(currency)
    except Exception as e:
        print(f"Ошибка при получении курса валюты: {e}")
        return None


def convert_transaction_to_rub(transaction):
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
        currency = transaction['operationAmount']['currency']['code']
    except KeyError as e:
        print(f"Ошибка: отсутствует ключ {e} в транзакции.")
        return 0.0

    if currency == 'RUB':
        return float(amount)  # Если валюта уже рубли, возвращаем сумму

    if currency in ['USD', 'EUR']:
        rate = get_exchange_rate(currency)
        if rate is not None:
            return float(amount) * rate  # Конвертация в рубли
        else:
            print(f"Не удалось получить курс для валюты: {currency}.")
            return 0.0

    print(f"Валюта {currency} не поддерживается для конвертации.")
    return 0.0  # Если валюта не поддерживается
