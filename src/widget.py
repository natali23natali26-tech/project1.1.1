import datetime
from typing import Union
# Import from utils.py

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(input_string: Union[str, int, None]) -> str:
    """
       Определяет тип карты или счета
       и маскирует номер в соответствии с его типом.

       Args:
           input_string: Строка с типом
           карты/счета и его номером.

       Returns:
           Строка с маскированным номером карты или счета.
           Например, "Visa Platinum 7000 79** **** 6361"
           или "Счет **3505"
       """

    result = ''

    if input_string is None:
        raise TypeError('Вводные данные отсутствуют.')

    if not isinstance(input_string, str):
        raise TypeError('Введена не строка')

    words = input_string.split()

    for word in words:
        if word.isalpha():
            result += word + ' '
        elif word.isdigit():
            if result == 'Счет':
                account_number = int(word)
                masked_account = get_mask_account(account_number)
            else:
                account_number = int(word)
                masked_account = get_mask_card_number(account_number)

    return f'{result} {masked_account}'

    # parts = input_string.split()
    # card_type = ' '.join(parts[:-1])
    # card_number_str = parts[-1]

    # Вызов функции с проверкой
    # if card_type in ['Visa', 'Maestro', 'MasterCard', 'МИР', 'Visa Classic', 'Visa Platinum', 'Visa Gold']:
    #     masked_number = get_mask_card_number(card_number_str)
    #     return f"{card_type} {masked_number}"
    # elif 'Счет' in card_type:
    #     # Для счетов считаем, что номер тоже в виде числа
    #     try:
    #         account_number = int(card_number_str)
    #         masked_account = get_mask_account(account_number)
    #         return f"{card_type} {masked_account}"
    #     except ValueError:
    #         return "Некорректный номер счета"
    # else:
    #     raise ValueError(f"Неизвестный тип карты или счета: {card_type}")


def get_date(date_string: str) -> str:
    """
    Преобразует строку даты из формата
     "2024-03-11T02:26:18.671407"
     в формат
      "ДД.ММ.ГГГГ" ("11.03.2024").

    Args:
        date_string:
        Дата в формате
        "2024-03-11T02:26:18.671407".

    Returns:
        Дата в формате
        "ДД.ММ.ГГГГ" ("11.03.2024").
    """
    try:
        date_object = datetime.datetime.fromisoformat(
            date_string.replace('Z', '+00:00')
        )  # Handle Z timezone
        return date_object.strftime('%d.%m.%Y')
    except ValueError:
        return "Неверный формат даты"


if __name__ == "__main__":
    input_card = "Visa Platinum 7000792289606361"
    masked_card = mask_account_card(input_card)
    print(f"{input_card} -> {masked_card}")
