def get_mask_card_number(card_number: int) -> str:
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


def get_mask_account(account_number: int) -> str:
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


if __name__ == "__main__":
    card_number = 1234567890123456
    masked_card = get_mask_card_number(card_number)
    print(f"Маскированный номер карты: {masked_card}")

    account_number = 1234567890
    masked_account = get_mask_account(account_number)
    print(f"Маскированный номер счета: {masked_account}")

