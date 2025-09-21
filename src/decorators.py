import functools
import logging
import sys


def log(filename=None):
    """
    Декоратор для логирования работы функции, её результатов и ошибок.

    Параметры:
    filename : str or None - имя файла для записи логов
    """
    # Настройка логирования
    if filename:
        logging.basicConfig(filename=filename, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Логируем начало выполнения функции
            logging.info(f"Start execution of {func.__name__} with args: {args} and kwargs: {kwargs}")
            try:
                # Выполняем функцию
                result = func(*args, **kwargs)
                # Логируем успешное завершение с результатом
                logging.info(f"{func.__name__} ok; result: {result}")
                return result
            except Exception as e:
                # Логируем ошибку, тип ошибки и входные параметры
                logging.error(f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}")
                raise  # Пробрасываем исключение дальше

        return wrapper

    return decorator
