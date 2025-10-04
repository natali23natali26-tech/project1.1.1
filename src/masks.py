import logging
import os


# Настройка логирования
def setup_logging():
    # Создаем папку для логов, если она не существует
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Формат логирования
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(
        filename='logs/app.log',  # Путь к файлу лога
        level=logging.DEBUG,  # Уровень логирования
        format=log_format,  # Формат записи
        filemode='w'  # Перезаписывать файл при каждом запуске
    )


# Функция для маскирования номера карты
def get_mask_card_number(card_number: int) -> str:
    """
    Маскирует номер карты по правилу XXXX XX** **** XXXX.

    Args:
        card_number (int): Номер карты в виде целого числа.

    Returns:
        str: Маскированный номер карты в виде строки.
    """
    card_number_str = str(card_number)
    if len(card_number_str) != 16:
        logging.error("Номер карты должен содержать 16 цифр.")
        raise ValueError("Номер карты должен содержать 16 цифр.")

    masked_number = (
            card_number_str[:4]
            + " "
            + card_number_str[4:6]
            + "** **** "
            + card_number_str[12:]
    )

    logging.info(f"Замаскированный номер карты: {masked_number}")
    return masked_number


# Функция для маскирования номера счета
def get_mask_account(account_number: int) -> str:
    """
    Маскирует номер счета по правилу **XXXX.

    Args:
        account_number (int): Номер счета в виде целого числа.

    Returns:
        str: Маскированный номер счета в виде строки.
    """
    account_number_str = str(account_number)
    masked_account = "**" + account_number_str[-4:]

    logging.info(f"Замаскированный номер счета: {masked_account}")
    return masked_account


if __name__ == "__main__":
    setup_logging()  # Настройка логирования

    try:
        card_number = 1234567890123456
        masked_card = get_mask_card_number(card_number)
        print(f"Маскированный номер карты: {masked_card}")

        account_number = 1234567890
        masked_account = get_mask_account(account_number)
        print(f"Маскированный номер счета: {masked_account}")

    except Exception as e:
        logging.exception("Произошла ошибка: %s", e)
