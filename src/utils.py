import json
import os
import logging


# Настройка логирования
def setup_logging():
    # Создаем папку для логов, если она не существует
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Основной логер приложения
    main_log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(
        filename='logs/app.log',  # Путь к файлу лога
        level=logging.DEBUG,  # Уровень логирования
        format=main_log_format,  # Формат записи
        filemode='w'  # Перезаписывать файл при каждом запуске
    )

    # Настройка логера для модуля utils
    utils_logger = logging.getLogger('utils')
    utils_logger.setLevel(logging.DEBUG)  # Уровень логирования не менее DEBUG

    # Настройка обработчика для логера модуля utils
    file_handler = logging.FileHandler('logs/utils.log')
    file_handler.setLevel(logging.DEBUG)  # Уровень обработчика

    # Настройка формата для логера модуля utils
    file_formatter = logging.Formatter(main_log_format)
    file_handler.setFormatter(file_formatter)

    # Добавляем обработчик к логеру
    utils_logger.addHandler(file_handler)

    return utils_logger  # Возвращаем логер для дальнейшего использования


def load_transactions(file_path):
    """
    Загружает финансовые транзакции из указанного JSON-файла.

    :param file_path: Путь до JSON-файла, который содержит транзакции.
    :return: Список словарей с данными о транзакциях или пустой список,
             если файл пустой, не найден или имеет неправильный формат.
    """
    utils_logger = logging.getLogger('utils')

    # Проверяем, существует ли файл по указанному пути
    if not os.path.exists(file_path):
        utils_logger.error(f"Файл не найден: {file_path}")
        return []

    # Попробуем открыть и прочитать файл
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        utils_logger.error("Ошибка при декодировании JSON. Проверьте формат файла.")
        return []
    except FileNotFoundError:
        utils_logger.error(f"Ошибка: файл не найден по пути: {file_path}.")
        return []
    except Exception as e:
        utils_logger.error(f"Ошибка при чтении файла: {e}")
        return []

    # Проверяем, являются ли прочитанные данные списком
    if not isinstance(data, list):
        utils_logger.error("Данные в файле не представляют собой список.")
        return []

    utils_logger.info("Транзакции успешно загружены.")
    return data


def convert_to_rub(transaction):
    """
    Конвертирует сумму транзакции в рубли на основе валютного курса.

    :param transaction: Словарь с данными о транзакции,
                       должен содержать ключи 'operationAmount.amount' и 'operationAmount.currency.code'.
    :return: Сумма транзакции в рублях как float.
    """
    utils_logger = logging.getLogger('utils')

    try:
        # Извлекаем сумму и код валюты из вложенной структуры
        amount = transaction.get('operationAmount', {}).get('amount')
        currency = transaction.get('operationAmount', {}).get('currency', {}).get('code')

        if amount is None or currency is None:
            raise KeyError("Отсутствует обязательное поле amount или currency")

        amount = float(amount)  # Преобразуем в число сразу после извлечения
    except (KeyError, TypeError) as e:
        utils_logger.error(f"Ошибка: отсутствует ключ {e} в транзакции или некорректный тип данных.")
        return 0.0

    if currency == 'RUB':
        utils_logger.info(f"Сумма в рублях: {amount}")
        return amount  # Если уже в рублях, просто возвращаем сумму

    # Получаем курс валюты через API
    rate = get_mock_exchange_rate(currency)  # Используем мок

    if rate is not None:
        rub_amount = amount * rate  # Конвертация в рубли
        utils_logger.info(f"Конвертировано {amount} {currency} в {rub_amount} RUB")
        return rub_amount
    else:
        utils_logger.error(f"Не удалось получить курс для валюты: {currency}.")
        return 0.0  # Возвращаем 0, если не удалось получить курс


def get_mock_exchange_rate(currency):
    """
    Возвращает моковый курс обмена для указанной валюты.
    В реальном коде здесь должен быть вызов внешнего API.
    """
    exchange_rates = {
        'USD': 90.0,
        'EUR': 100.0,
        'GBP': 110.0
    }
    return exchange_rates.get(currency)


if __name__ == "__main__":
    setup_logging()  # Настройка логирования

    # Пример работы с загрузкой и конвертацией
    transactions = load_transactions('transactions.json')

    for transaction in transactions:
        rub_amount = convert_to_rub(transaction)
        if rub_amount > 0:
            print(f"Сумма транзакции в рублях: {rub_amount}")
