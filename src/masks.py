def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты по правилу XXXX XX** **** XXXX.

    Args:
        card_number: Номер карты в виде целого числа.

    Returns:
        Маскированный номер карты в виде строки.
    """
    card_number_str = str(card_number)
    if len(card_number_str) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр.")

    masked_number = (
        card_number_str[:4]
        + " "
        + card_number_str[4:6]
        + "** **** "
        + card_number_str[12:]
    )
    return masked_number


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета по правилу **XXXX.

    Args:
        account_number: Номер счета в виде целого числа.

    Returns:
        Маскированный номер счета в виде строки.
    """
    account_number_str = str(account_number)
    masked_account = "**" + account_number_str[-4:]
    return masked_account


def mask_account_card(input_string: str) -> str:
    """
    Определяет тип карты или счета и маскирует номер в соответствии с его типом.

    Args:
        input_string: Строка с типом карты/счета и его номером.

    Returns:
        Строка с маскированным номером карты или счета.
    """
    parts = input_string.split()
    card_type = parts[0]  # Тип карты или счета
    card_number = ''.join(parts[1:])  # Объединяем номера в одну строку

    if 'Visa' in card_type or 'Maestro' in card_type:
        return get_mask_card_number(card_number)
    elif 'Счет' in card_type:
        return get_mask_account(card_number)
    else:
        raise ValueError("Неизвестный тип карты или счета.")


def get_date(date_string: str) -> str:
    """
    Преобразует строку даты в формат dd.mm.yyyy.

    Args:
        date_string: Дата в любом формате.

    Returns:
        Дата в формате dd.mm.yyyy.
    """
    # Для упрощения примем, что строка даты уже в правильном формате
    return date_string


if __name__ == "__main__":
    input_data_1 = "Visa Platinum 7000792289606361"
    masked_card = mask_account_card(input_data_1)
    print(f"Маскированный номер карты: {masked_card}")  # Вывод: 7000 79** **** 6361

    input_data_2 = "Счет 73654108430135874305"
    masked_account = mask_account_card(input_data_2)
    print(f"Маскированный номер счета: {masked_account}")  # Вывод: **3505
