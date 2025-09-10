import pytest
from masks import get_mask_card_number, get_mask_account

# Тестирование функции get_mask_card_number
@pytest.mark.parametrize(
    "card_number, expected_output",
    [
        (1234567890123456, "1234 56** **** 3456"),
        (9876543210123456, "9876 54** **** 3456"),
        (1111222233334444, "1111 22** **** 4444"),
    ],
)
def test_get_mask_card_number_valid(card_number, expected_output):
    """
    Тестируется функция get_mask_card_number с валидными входными данными.
    """
    assert get_mask_card_number(card_number) == expected_output

@pytest.mark.parametrize(
    "card_number, expected_exception",
    [
        (123456789012345, ValueError),  # менее 16 цифр
        (12345678901234567, ValueError),  # более 16 цифр
        ("abcd123456789012", ValueError),  # некорректные символы
        (None, ValueError)  # отсутствующий номер карты
    ],
)
def test_get_mask_card_number_invalid(card_number, expected_exception):
    """
    Тестируется функция get_mask_card_number с невалидными входными данными.
    """
    with pytest.raises(expected_exception):
        get_mask_card_number(card_number)


# Тестирование функции get_mask_account
@pytest.mark.parametrize(
    "account_number, expected_output",
    [
        (1234567890, "**7890"),
        (987654321, "**4321"),
        (1111, "**1111"),  # Проверка на короткой длине
    ],
)
def test_get_mask_account_valid(account_number, expected_output):
    """
    Тестируется функция get_mask_account с валидными входными данными.
    """
    assert get_mask_account(account_number) == expected_output

@pytest.mark.parametrize(
    "account_number, expected_exception",
    [
        (123, ValueError),  # номер меньше 4-х цифр
        ("abcd1234", ValueError),  # некорректные символы
        (None, ValueError)  # отсутствующий номер счета
    ],
)
def test_get_mask_account_invalid(account_number, expected_exception):
    """
    Тестируется функция get_mask_account с невалидными входными данными.
    """
    with pytest.raises(expected_exception):
        get_mask_account(account_number)
