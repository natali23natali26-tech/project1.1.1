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
        response.raise_for_status()  # Вызывает исключение для кода ответа >= 400
        data = response.json()
        return data['rates'].get(currency)  # Возвращаем курс для указанной валюты
    except Exception as e:
        print(f"Ошибка при получении курса валюты: {e}")
        return None
