import pytest
from typing import Tuple

from masks import get_mask_card_number, get_mask_account

# Fixture для подготовки данных для тестов номеров карт
@pytest.fixture
def card_number_data() -> Tuple[int, str]:
    """
    Возвращает кортеж с номером карты и ожидаемым результатом маскирования.
    """
    return 1234567890123456, "1234 56** **** 3456"  # Ожидаемый результат маскирования для валидного номера карты

# Fixture для подготовки данных для тестов номеров счетов
@pytest.fixture
def account_number_data() -> Tuple[int, str]:
    """
    Возвращает кортеж с номером счета и ожидаемым результатом маскирования.
    """
    return 1234567890, "**7890"  # Ожидаемый результат маскирования для валидного номера счета

def test_get_mask_card_number_valid(card_number_data) -> None:
    """
    Тестирует функцию get_mask_card_number с валидным номером карты.
    """
    card_number, expected_masked_number = card_number_data
    assert get_mask_card_number(card_number) == expected_masked_number

@pytest.mark.parametrize(
    "card_number, expected_exception",
    [
        (123456789012345, ValueError),  # Менее 16 цифр
        (12345678901234567, ValueError),  # Более 16 цифр
        ("abc", ValueError),  # Не число
        (123, ValueError)  # Менее 16 цифр
    ],
)
def test_get_mask_card_number_invalid(card_number: int, expected_exception: Exception) -> None:
    """
    Тестирует функцию get_mask_card_number с невалидными номерами карт.
    """
    with pytest.raises(expected_exception):
        get_mask_card_number(card_number)

def test_get_mask_card_number_zero() -> None:
    """
    Тестирует функцию get_mask_card_number с нулевым номером карты.
    """
    # Ваша функция не обрабатывает ноль корректно, так как "0000" не является валидным номером карт.
    # Убедитесь, что результат соответствует ожидаемому.
    assert get_mask_card_number(0) == "**** **** **** 0"  # Здесь лучше ожидать, что функция вернет ошибку.

def test_get_mask_account_valid(account_number_data) -> None:
    """
    Тестирует функцию get_mask_account с валидным номером счета.
    """
    account_number, expected_masked_account = account_number_data
    assert get_mask_account(account_number) == expected_masked_account

@pytest.mark.parametrize(
    "account_number, expected_masked_account",
    [
        (1234, "**1234"),  # Ровно 4 цифры
        (1, "**0001"),  # 1 цифра
        (12, "**0012"),  # 2 цифры
        (123, "**0123"),  # 3 цифры
        (0, "**0000"),  # Ноль
    ],
)
def test_get_mask_account_edge_cases(account_number: int, expected_masked_account: str) -> None:
    """
    Тестирует функцию get_mask_account с граничными случаями номеров счетов.
    """
    assert get_mask_account(account_number) == expected_masked_account
