import functools
import logging
import sys


def log(filename=None):
    """
    Декоратор для логирования работы функции, её результатов и ошибок.

    Этот декоратор оборачивет функцию, логируя ее вызовы, возвращаемые значения и любые исключения,
    которые она может вызвать.  Логи записываются либо в указанный файл, либо в стандартный поток вывода.

    Args:
        filename (str, optional): Имя файла для записи логов. Если не указано (None), логи будут выводиться в stdout.
                                    Defaults to None.

    Returns:
        callable: Декоратор, который можно применить к функции.

    Example:
        @log(filename="my_log.txt")
        def my_function(x, y):
            return x + y
    """
    # Настройка логирования
    if filename:
        logging.basicConfig(filename=filename, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def decorator(func):
        """
        Внутренний декоратор, который оборачивает функцию и добавляет логирование.

        Args:
            func (callable): Функция, которую нужно обернуть.

        Returns:
            callable: Обернутая функция с логированием.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """
            Обертка для функции, выполняющая логирование.

            Args:
                *args: Позиционные аргументы, переданные в оборачиваемую функцию.
                **kwargs: Именованные аргументы, переданные в оборачиваемую функцию.

            Returns:
                Any: Результат выполнения оборачиваемой функции.

            Raises:
                Exception: Если оборачиваемая функция вызывает исключение, оно будет перехвачено,
                           залогировано и снова вызвано (re-raised).
            """
            # Логируем начало выполнения функции
            logging.info(f"Start execution of {func.__name__} with args: {args} and kwargs: {kwargs}")
            try:
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
