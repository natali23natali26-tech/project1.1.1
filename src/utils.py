import json
import os
from src.external_api import get_exchange_rate


def load_transactions(file_path):
    """
    Загружает финансовые транзакции из указанного JSON-файла.

    Проверяет наличие файла по указанному пути, пытается открыть и прочитать его.
    Если файл не найден, пуст или имеет неправильный формат, возвращает пустой список.

    :param file_path: Путь до JSON-файла, который содержит транзакции.
    :return: Список словарей с данными о транзакциях или пустой список,
             если файл пустой, не найден или имеет неправильный формат.
    """
    # Проверяем, существует ли файл по указанному пути
    if not os.path.exists(file_path):
        print(f"Файл не найден: {file_path}")
        return []

    # Попробуем открыть и прочитать файл
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print("Ошибка при декодировании JSON. Проверьте формат файла.")
        return []
    except FileNotFoundError:
        print(f"Ошибка: файл не найден по пути: {file_path}.")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []

    # Проверяем, являются ли прочитанные данные списком
    if not isinstance(data, list):
        print("Данные в файле не представляют собой список.")
        return []

    return data


def convert_to_rub(transaction):
    """
    Конвертирует сумму транзакции в рубли на основе валютного курса.

    Если валюта транзакции уже является рублем, просто возвращает сумму.
    В противном случае, извлекает сумму и валюту из вложенного словаря и запрашивает курс валюты.
    Если не удается получить курс, возвращает 0.0.

    :param transaction: Словарь с данными о транзакции,
                       должен содержать ключи 'operationAmount.amount' и 'operationAmount.currency.code'.
    :return: Сумма транзакции в рублях как float.
             Если валюта неизвестна или возникает ошибка, возвращает 0.0.
    """
    try:
        # Извлекаем сумму и код валюты из вложенной структуры
        amount = transaction['operationAmount']['amount']
        currency = transaction['operationAmount']['currency']['code']
    except KeyError as e:
        print(f"Ошибка: отсутствует ключ {e} в транзакции.")
        return 0.0

    if currency == 'RUB':
        return float(amount)  # Если уже в рублях, просто возвращаем сумму

    # Получаем курс валюты через API
    rate = get_exchange_rate(currency)

    if rate is not None:
        return float(amount) * rate  # Конвертация в рубли
    else:
        print(f"Не удалось получить курс для валюты: {currency}.")
        return 0.0  # Возвращаем 0, если не удалось получить курс
