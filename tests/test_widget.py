import pytest
from src.widget import mask_account_card, get_date

# Тестирование функции mask_account_card
@pytest.mark.parametrize(
    "input_string, expected_output",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("MasterCard 1234567812345678", "MasterCard 1234 56** **** 5678"),
        ("Maestro 1234567890123456", "Maestro 1234 56** **** 3456"),
        ("Счет 1234567890", "Счет **7890"),
        ("Счет 9876543210", "Счет **3210"),
    ],
)
def test_mask_account_card_valid(input_string, expected_output):
    """
    Тестирует функцию mask_account_card с валидными входными данными.
    """
    assert mask_account_card(input_string) == expected_output

@pytest.mark.parametrize(
    "input_string, expected_output",
    [
        ("UnknownType 1234567890", ValueError),  # Неизвестный тип
        ("Visa 123abc", "Неверный формат номера карты/счета"),  # Некорректный номер
        ("Счет not_a_number", "Неверный формат номера карты/счета"),  # Некорректный номер
        ("", ValueError)  # Пустая строка ожидает ValueError
    ],
)
def test_mask_account_card_invalid(input_string, expected_output):
    """
    Тестирует функцию mask_account_card с невалидными входными данными.
    """
    if isinstance(expected_output, type) and issubclass(expected_output, Exception):
        with pytest.raises(expected_output):
            mask_account_card(input_string)
    else:
        assert mask_account_card(input_string) == expected_output

# Тестирование функции get_date
@pytest.mark.parametrize(
    "date_string, expected_output",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2022-01-01T00:00:00Z", "01.01.2022"),  # Обработка Z в конце
        ("2023-12-31T23:59:59", "31.12.2023"),
    ],
)
def test_get_date_valid(date_string, expected_output):
    """
    Тестирует функцию get_date с валидными входными данными.
    """
    assert get_date(date_string) == expected_output

@pytest.mark.parametrize(
    "date_string, expected_output",
    [
        ("invalid_date", "Неверный формат даты"),  # Некорректный формат
        ("", "Неверный формат даты"),  # Пустая строка
        ("2024-13-01T00:00:00", "Неверный формат даты"),  # Месяц вне диапазона
        ("2024-02-30T00:00:00", "Неверный формат даты"),  # Некорректная дата
    ],
)
def test_get_date_invalid(date_string, expected_output):
    """
    Тестирует функцию get_date с невалидными входными данными.
    """
    assert get_date(date_string) == expected_output
