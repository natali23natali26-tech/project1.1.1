import datetime

# Import from utils.py
from .masks import get_mask_account, get_mask_card_number


def mask_account_card(input_string: str) -> str:
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
    parts = input_string.split()
    card_type = ' '.join(parts[:-1])
    card_number_str = parts[-1]  # Номер как строка

    try:
        # Преобразуем в int для совместимости
        card_number = int(card_number_str)
    except ValueError:
        return "Неверный формат номера карты/счета"

    if ('Visa' in card_type or 'Maestro'
            in card_type or 'MasterCard' in card_type):
        # Use the imported functions
        masked_number = get_mask_card_number(card_number)
        return f"{card_type} {masked_number}"
    elif 'Счет' in card_type:
        # Use the imported functions
        masked_account = get_mask_account(card_number)
        return f"{card_type} {masked_account}"
    else:
        raise ValueError("Неизвестный тип карты или счета.")


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
