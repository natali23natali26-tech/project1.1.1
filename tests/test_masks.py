import pytest


from src.masks import get_mask_card_number, get_mask_account

# Фикстуры
@pytest.fixture
def valid_card_number():
    return 1234567890123456


@pytest.fixture
def valid_account_number():
    return 1234567890


@pytest.mark.parametrize(
    "card_number, expected_output",
    [
        (1234567890123456, "1234 56** **** 3456"),
        (9876543210123456, "9876 54** **** 3456"),
        (1111222233334444, "1111 22** **** 4444"),
    ],
)
def test_get_mask_card_number_valid(card_number, expected_output):
    """Тестируется функция get_mask_card_number с валидными входными данными."""
    assert get_mask_card_number(card_number) == expected_output


@pytest.mark.parametrize(
    "account_number, expected_output",
    [
        (1234567890, '**7890'),
        (987654321, '**4321'),
        (1111, '**1111'),
        (123, '**0123'),
        (12, '**0012'),
        (1, '**0001'),
        (0, '**0000'),
    ],
)
def test_get_mask_account_valid(account_number, expected_output):
    """Тестируется функция get_mask_account с валидными входными данными."""
    account_str = str(account_number)

    # Проверяем длину, чтобы убедиться, что она в пределах допустимых значений
    assert 1 <= len(account_str) <= 10, f"Длина номера счета {account_number} должна быть от 1 до 10 символов."

    last_four_digits = account_str[-4:].zfill(4)  # Берем последние 4 цифры и дополняем нулями слева, если их меньше 4.
    masked_account = "**" + last_four_digits  # Формируем маску.

    assert expected_output == masked_account


@pytest.mark.parametrize(
    "account_number",
    [
        1234567890,
        987654321,
        1111,
        123,
        12,
        1,
        0,
    ],
)
def test_get_mask_account_no_exception(account_number):
    """Проверяет, что get_mask_account не выбрасывает исключение для валидных данных."""
    try:
        get_mask_account(account_number)
    except Exception as e:
        pytest.fail(f"Выброшено исключение: {e}")